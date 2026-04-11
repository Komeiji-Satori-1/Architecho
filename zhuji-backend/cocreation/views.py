from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import CoCreationItem, CoCreationImage
from .serializers import (
    CoCreationNewsSerializer,
    CoCreationListSerializer,
    CoCreationAuditSerializer,
    CoCreationDetailSerializer,
)


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('superadmin', 'moderator')
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recent_news(request):
    """
    首页「共创动态」：返回最近采纳的 2 条共创。
    GET /api/cocreation/recent-news/
    返回：[{id, type, label, content}, ...]
    """
    items = (
        CoCreationItem.objects
        .filter(status=CoCreationItem.STATUS_ADOPTED)
        .select_related('author')
        .order_by('-updated_at')[:2]
    )
    serializer = CoCreationNewsSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_progress(request):
    """
    当前用户的共创进度列表。
    GET /api/cocreation/my-progress/
    """
    items = (
        CoCreationItem.objects
        .filter(author=request.user)
        .select_related('author')
        .order_by('-created_at')
    )
    serializer = CoCreationListSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)


class CoCreationItemViewSet(viewsets.ModelViewSet):
    queryset = CoCreationItem.objects.select_related('author').all()
    serializer_class = CoCreationListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            qs = qs.filter(featured=True)
        return qs

    def perform_create(self, serializer):
        item = serializer.save(author=self.request.user)
        # 处理灵感图上传（multipart 中 images 字段）
        images = self.request.FILES.getlist('images')
        for idx, img in enumerate(images):
            CoCreationImage.objects.create(item=item, image=img, sort_order=idx)

    @action(detail=True, methods=['post'], url_path='audit', permission_classes=[IsAdminUser])
    def audit(self, request, pk=None):
        """
        审核/推进共创筑品状态。
        payload: { status: 'reviewing'|'sampling'|'producing'|'adopted'|'rejected', progress_percent?: 0-100 }
        """
        item = self.get_object()
        serializer = CoCreationAuditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item.status = serializer.validated_data['status']
        update_fields = ['status']

        if 'progress_percent' in serializer.validated_data:
            item.progress_percent = serializer.validated_data['progress_percent']
            update_fields.append('progress_percent')

        item.save(update_fields=update_fields)
        return Response(CoCreationDetailSerializer(
            item, context={'request': request}
        ).data)
