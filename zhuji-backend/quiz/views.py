from rest_framework import viewsets, permissions, filters
from .models import QuizQuestion
from .serializers import QuizQuestionSerializer, QuizQuestionWriteSerializer


class QuizQuestionViewSet(viewsets.ModelViewSet):
    """
    题库题目 CRUD ViewSet。
    - GET list/retrieve：所有认证用户均可查看（用于前端答题页）
    - POST/PUT/PATCH/DELETE：仅管理员可操作（对应后台题库管理面板）
    """
    queryset = QuizQuestion.objects.select_related('monument').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'correct_answer', 'monument__title']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return QuizQuestionWriteSerializer
        return QuizQuestionSerializer
