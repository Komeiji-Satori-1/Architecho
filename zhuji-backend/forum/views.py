from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import ForumCategory, ForumPost, Comment, PostImage
from .serializers import (
    ForumCategorySerializer,
    ForumPostHotSerializer,
    ForumPostListSerializer,
    ForumPostDetailSerializer,
    ForumPostCreateSerializer,
    CommentSerializer,
)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def hot_topics(request):
    """
    首页热门话题：按浏览量降序取前 5 篇。
    GET /api/forum/hot-topics/
    返回：[{id, title, author, reads}, ...]
    """
    posts = (
        ForumPost.objects.select_related('author')
        .order_by('-views')[:5]
    )
    serializer = ForumPostHotSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


class ForumCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ForumCategory.objects.all()
    serializer_class = ForumCategorySerializer
    permission_classes = [permissions.AllowAny]


class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.select_related('author', 'category').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ForumPostDetailSerializer
        if self.action == 'create':
            return ForumPostCreateSerializer
        return ForumPostListSerializer

    def get_queryset(self):
        qs = super().get_queryset().order_by('-created_at')
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__id=category)
        is_essence = self.request.query_params.get('is_essence')
        if is_essence == 'true':
            qs = qs.filter(is_essence=True)
        ordering = self.request.query_params.get('ordering')
        if ordering in ('-created_at', 'created_at', '-views', 'views'):
            qs = qs.order_by(ordering)
        return qs


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """POST /api/forum/posts/:id/like/ — 点赞/取消点赞（简化版）"""
        post = self.get_object()
        post.likes += 1
        post.save(update_fields=['likes'])
        return Response({'likes': post.likes})

    @action(detail=True, methods=['post'], url_path='images',
            permission_classes=[permissions.IsAuthenticated])
    def upload_images(self, request, pk=None):
        """POST /api/forum/posts/:id/images/ — 上传多张正文配图"""
        post = self.get_object()
        if post.author != request.user:
            return Response({'detail': '无权操作。'}, status=status.HTTP_403_FORBIDDEN)
        files = request.FILES.getlist('images')
        if not files:
            return Response({'detail': '请选择图片。'}, status=status.HTTP_400_BAD_REQUEST)
        from .models import PostImage
        created = []
        for idx, f in enumerate(files):
            img = PostImage.objects.create(post=post, image=f, sort_order=idx)
            created.append(img.id)
        return Response({'uploaded': len(created)}, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author').filter(parent=None)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post__id=post_id)
        return qs

    def perform_create(self, serializer):
        parent_id = self.request.data.get('parent')
        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                pass
        serializer.save(author=self.request.user, parent=parent)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        user = request.user
        from users.models import User
        is_superadmin = hasattr(user, 'role') and user.role == User.ROLE_SUPERADMIN
        if comment.author != user and not is_superadmin:
            return Response({'detail': '无权删除他人评论。'}, status=status.HTTP_403_FORBIDDEN)
        # 一级评论删除时，Django CASCADE 会自动删除其所有二级回复
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='images',
            permission_classes=[permissions.IsAuthenticated])
    def upload_images(self, request, pk=None):
        """POST /api/forum/comments/:id/images/ — 上传一级评论配图（最多5张）"""
        comment = self.get_object()
        if comment.parent is not None:
            return Response({'detail': '二级回复不支持图片上传。'}, status=status.HTTP_400_BAD_REQUEST)
        if comment.author != request.user:
            return Response({'detail': '无权操作。'}, status=status.HTTP_403_FORBIDDEN)
        files = request.FILES.getlist('images')
        if not files:
            return Response({'detail': '请选择图片。'}, status=status.HTTP_400_BAD_REQUEST)
        from .models import CommentImage
        existing = comment.images.count()
        remaining = 5 - existing
        if remaining <= 0:
            return Response({'detail': '已达到5张上限。'}, status=status.HTTP_400_BAD_REQUEST)
        for idx, f in enumerate(files[:remaining]):
            CommentImage.objects.create(comment=comment, image=f, sort_order=existing + idx)
        return Response({'uploaded': min(len(files), remaining)}, status=status.HTTP_201_CREATED)
