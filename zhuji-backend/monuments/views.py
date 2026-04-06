from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Monument, ArticleSubmission
from .serializers import (
    MonumentSerializer,
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
