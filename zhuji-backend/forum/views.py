from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import ForumCategory, ForumPost, Comment
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
