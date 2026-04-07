from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Monument, ArticleSubmission, MonumentArticle, MonumentArticlePage, UserMonumentProgress
from .serializers import (
    MonumentSerializer,
    MonumentDiscoverySerializer,
    MonumentArticleSerializer,
    MonumentArticleWriteSerializer,
    MonumentArticlePageWriteSerializer,
    SubmissionListSerializer,
    SubmissionDetailSerializer,
    SubmissionAuditSerializer,
)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_monument(request):
    """
    首页 Hero 推荐古建：返回最新发布的一条。
    GET /api/monuments/featured/
    """
    monument = Monument.objects.filter(is_published=True).order_by('-created_at')[:3]
    if not monument:
        return Response({'detail': '暂无推荐古建。'}, status=404)
    serializer = MonumentSerializer(monument, context={'request': request}, many=True)
    return Response(serializer.data)


class MonumentViewSet(viewsets.ModelViewSet):
    """
    古建条目 CRUD。
    只读操作对所有人开放，写操作仅管理员/版主。
    """
    queryset = Monument.objects.all()
    serializer_class = MonumentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'dynasty', 'location']
    ordering_fields = ['created_at', 'name']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    用户投稿 ViewSet。
    - list：支持按 status 筛选，审核中心使用
    - audit：自定义操作，一次性提交审核结论（通过/驳回 + 反馈）
    - quick_approve：快速通过（对应前端"快速通过"按钮）
    """
    queryset = ArticleSubmission.objects.select_related('author').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__username']
    ordering_fields = ['time', 'status']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'list':
            return SubmissionListSerializer
        if self.action == 'audit':
            return SubmissionAuditSerializer
        return SubmissionDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], url_path='audit')
    def audit(self, request, pk=None):
        """
        审核操作：payload { status: 'approved'|'rejected', feedback: '...' }
        对应前端"通过 / 驳回 + 输入反馈审核建议"流程。
        """
        submission = self.get_object()
        serializer = SubmissionAuditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission.status = serializer.validated_data['status']
        submission.feedback = serializer.validated_data['feedback']
        submission.save(update_fields=['status', 'feedback'])
        return Response(SubmissionDetailSerializer(
            submission, context={'request': request}
        ).data)

    @action(detail=True, methods=['post'], url_path='quick-approve')
    def quick_approve(self, request, pk=None):
        """快速通过：对应前端审核大盘中的"快速通过"按钮。"""
        submission = self.get_object()
        if submission.status != ArticleSubmission.STATUS_PENDING:
            return Response(
                {'detail': '仅待处理投稿可执行快速通过。'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        submission.status = ArticleSubmission.STATUS_APPROVED
        submission.save(update_fields=['status'])
        return Response({'detail': '投稿已通过。'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def discovery_monuments(request):
    """
    探索视窗古建列表 — 按用户探索进度排序。
    未完成的优先展示，已完成的需通过 ?include_completed=true 查看。
    """
    monuments = Monument.objects.filter(is_published=True)
    include_completed = request.query_params.get('include_completed', 'false') == 'true'

    # 预取当前用户进度
    progress_map = {}
    user_progresses = UserMonumentProgress.objects.filter(user=request.user)
    for p in user_progresses:
        progress_map[p.monument_id] = p

    result = []
    for m in monuments:
        m._user_progress = progress_map.get(m.id)
        progress = m._user_progress
        if not include_completed and progress and progress.status == 'completed':
            continue
        result.append(m)

    # 排序：进行中 > 未开始 > 已完成
    order = {'in_progress': 0, 'pending': 1, 'completed': 2}
    result.sort(key=lambda m: order.get(
        getattr(m._user_progress, 'status', 'pending') if m._user_progress else 'pending', 1
    ))

    serializer = MonumentDiscoverySerializer(result, many=True, context={'request': request})
    return Response(serializer.data)


class MonumentArticleViewSet(viewsets.ModelViewSet):
    """古建详细文章 CRUD"""
    queryset = MonumentArticle.objects.select_related('monument').prefetch_related('pages').all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'monument__name']

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'by_monument'):
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return MonumentArticleWriteSerializer
        return MonumentArticleSerializer

    @action(detail=False, methods=['get'], url_path='by-monument/(?P<monument_id>[0-9]+)')
    def by_monument(self, request, monument_id=None):
        """通过古建 ID 获取其文章"""
        try:
            article = MonumentArticle.objects.select_related('monument').prefetch_related(
                'pages__quiz_questions__options'
            ).get(monument_id=monument_id)
        except MonumentArticle.DoesNotExist:
            return Response({'detail': '该古建暂无详细文章。'}, status=404)
        return Response(MonumentArticleSerializer(article, context={'request': request}).data)

    @action(detail=True, methods=['get'], url_path='consistency-check')
    def consistency_check(self, request, pk=None):
        """检查文章页数对应的题目数与印章层数是否一致"""
        article = self.get_object()
        page_count = article.pages.count()
        quiz_count = sum(p.quiz_questions.count() for p in article.pages.all())
        stamp = article.monument.stamps.first() if article.monument else None
        layer_count = stamp.total_layers if stamp else 0
        consistent = quiz_count == layer_count
        return Response({
            'page_count': page_count,
            'quiz_count': quiz_count,
            'layer_count': layer_count,
            'consistent': consistent,
            'message': '一致' if consistent else f'不一致：题目数({quiz_count}) ≠ 印章层数({layer_count})',
        })


class MonumentArticlePageViewSet(viewsets.ModelViewSet):
    """文章页 CRUD"""
    queryset = MonumentArticlePage.objects.all()
    serializer_class = MonumentArticlePageWriteSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        qs = super().get_queryset()
        article_id = self.request.query_params.get('article')
        if article_id:
            qs = qs.filter(article_id=article_id)
        return qs
