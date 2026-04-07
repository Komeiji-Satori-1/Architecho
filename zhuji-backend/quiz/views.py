from django.db import transaction
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import QuizQuestion, QuizOption, UserQuizRecord
from .serializers import (
    QuizQuestionSerializer,
    QuizQuestionWriteSerializer,
    QuizOptionWriteSerializer,
    AnswerSubmitSerializer,
)
from stamps.models import UserStamp, Stamp


class QuizQuestionViewSet(viewsets.ModelViewSet):
    queryset = QuizQuestion.objects.select_related('monument', 'article_page').prefetch_related('options').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'monument__name']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return QuizQuestionWriteSerializer
        return QuizQuestionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        monument_id = self.request.query_params.get('monument')
        if monument_id:
            qs = qs.filter(monument_id=monument_id)
        article_page_id = self.request.query_params.get('article_page')
        if article_page_id:
            qs = qs.filter(article_page_id=article_page_id)
        return qs


class QuizOptionViewSet(viewsets.ModelViewSet):
    queryset = QuizOption.objects.select_related('question').all()
    serializer_class = QuizOptionWriteSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        qs = super().get_queryset()
        question_id = self.request.query_params.get('question')
        if question_id:
            qs = qs.filter(question_id=question_id)
        return qs


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_answer(request):
    """
    提交答题：校验答案 → 记录 → 更新积分 → 解锁印章层。
    POST /api/quiz/submit-answer/
    Body: { question_id, selected_option_ids: [1, 2, ...] }
    """
    serializer = AnswerSubmitSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    question_id = serializer.validated_data['question_id']
    selected_ids = serializer.validated_data['selected_option_ids']

    try:
        question = QuizQuestion.objects.prefetch_related('options').get(id=question_id)
    except QuizQuestion.DoesNotExist:
        return Response({'detail': '题目不存在。'}, status=404)

    # 防止重复答题
    if UserQuizRecord.objects.filter(user=request.user, question=question).exists():
        return Response({'detail': '你已经回答过此题。'}, status=status.HTTP_400_BAD_REQUEST)

    # 判断正确性
    correct_ids = set(question.options.filter(is_correct=True).values_list('id', flat=True))
    user_ids = set(selected_ids)
    is_correct = correct_ids == user_ids
    points_earned = question.points if is_correct else 0

    with transaction.atomic():
        # 创建答题记录
        record = UserQuizRecord.objects.create(
            user=request.user,
            question=question,
            is_correct=is_correct,
            points_earned=points_earned,
        )
        selected_options = QuizOption.objects.filter(id__in=selected_ids)
        record.selected_options.set(selected_options)

        # 更新用户统计
        user = request.user
        user.quiz_total_count += 1
        if is_correct:
            user.quiz_correct_count += 1
            user.influence_power += points_earned
        user.save(update_fields=['quiz_total_count', 'quiz_correct_count', 'influence_power'])

        # 解锁印章层
        stamp_unlocked = False
        if is_correct and question.monument:
            stamp = Stamp.objects.filter(monument=question.monument).first()
            if stamp:
                user_stamp, created = UserStamp.objects.get_or_create(
                    user=request.user, stamp=stamp,
                    defaults={'unlocked_layers': 0},
                )
                if user_stamp.unlocked_layers < stamp.total_layers:
                    user_stamp.unlocked_layers += 1
                    user_stamp.save(update_fields=['unlocked_layers'])
                    stamp_unlocked = True

    return Response({
        'is_correct': is_correct,
        'points_earned': points_earned,
        'correct_option_ids': list(correct_ids),
        'stamp_unlocked': stamp_unlocked,
    })
