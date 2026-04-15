from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Prefetch, F, Value, FloatField, Count, ExpressionWrapper
from django.db.models.functions import Greatest, Power, ExtractDay
from .models import (
    ForumCategory, ForumPost, Comment, PostImage, CommentImage,
    ForumInteraction, CommentLike, PostReport, CommentReport
)
from .serializers import (
    ForumCategorySerializer,
    ForumPostHotSerializer,
    ForumPostListSerializer,
    ForumPostDetailSerializer,
    ForumPostCreateSerializer,
    CommentSerializer,
    InteractionSerializer,
    CommentLikeSerializer,
    PostReportSerializer,
    CommentReportSerializer,
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
        qs = super().get_queryset().annotate(
            comment_count_val=Count('comments'),
        ).order_by('-is_top', '-created_at')
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__id=category)
        is_essence = self.request.query_params.get('is_essence')
        if is_essence == 'true':
            qs = qs.filter(is_essence=True)
        ordering = self.request.query_params.get('ordering')
        if ordering == '-heat_score':
            # 热度 = views*0.2 + likes*0.3 + comments*0.5，按降序
            qs = qs.annotate(
                computed_heat=ExpressionWrapper(
                    F('views') * 0.2 + F('likes') * 0.3 + F('comment_count_val') * 0.5,
                    output_field=FloatField(),
                ),
            ).order_by('-computed_heat')
        elif ordering in ('-created_at', 'created_at', '-views', 'views'):
            qs = qs.order_by(ordering)
        return qs


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def interact(self, request, pk=None):
        """
        统一交互端点：点赞/取消点赞
        POST /api/forum/posts/{id}/interact/
        body: {"action": "like"|"unlike"}
        """
        post = self.get_object()
        action = request.data.get('action')
        print(f"[DEBUG-Interact] User {request.user.username} performing {action} on post {post.id}")
        
        if action == 'like':
            # 检查是否已点赞
            interaction, created = ForumInteraction.objects.get_or_create(
                user=request.user, post=post,
                interaction_type=ForumInteraction.LIKE
            )
            if created:
                post.likes += 1
                post.save(update_fields=['likes'])
                print(f"[DEBUG-Interact] New like created, total likes: {post.likes}")
                # 通知帖子作者（不通知自己）
                if post.author != request.user:
                    from users.models import Notification
                    Notification.objects.create(
                        user=post.author,
                        title=f'{request.user.username} 赞了你的帖子',
                        content=f'《{post.title}》获得了一个新的点赞',
                        notification_type=Notification.TYPE_LIKE,
                        triggered_by=request.user,
                    )
            else:
                print(f"[DEBUG-Interact] Like already exists")
            return Response({'likes': post.likes, 'action': 'liked', 'is_liked': True})
        
        elif action == 'unlike':
            try:
                interaction = ForumInteraction.objects.get(
                    user=request.user, post=post,
                    interaction_type=ForumInteraction.LIKE
                )
                interaction.delete()
                post.likes = max(0, post.likes - 1)
                post.save(update_fields=['likes'])
                print(f"[DEBUG-Interact] Like removed, total likes: {post.likes}")
            except ForumInteraction.DoesNotExist:
                print(f"[DEBUG-Interact] Like not found, nothing to remove")
                pass
            return Response({'likes': post.likes, 'action': 'unliked', 'is_liked': False})
        
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def report(self, request, pk=None):
        """
        举报帖子
        POST /api/forum/posts/{id}/report/
        body: {"reason": "举报原因"}
        """
        post = self.get_object()
        reason = request.data.get('reason', '')
        print(f"[DEBUG-Report] User {request.user.username} reporting post {post.id}")
        
        report = PostReport.objects.create(
            post=post,
            reported_by=request.user,
            reason=reason
        )
        serializer = PostReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        created = []
        for idx, f in enumerate(files):
            img = PostImage.objects.create(post=post, image=f, sort_order=idx)
            created.append(img.id)
        print(f"[DEBUG-Upload] {len(created)} images uploaded for post {post.id}")
        return Response({'uploaded': len(created)}, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related('author')
        replies_qs = Comment.objects.select_related('author').order_by('created_at')
        qs = qs.prefetch_related(
            'images', # 预加载图片
            Prefetch('replies', queryset=replies_qs) # 预加载回复及其作者
        )
        if self.action == 'list':
            # 如果是获取某个帖子的评论列表，只看一级评论
            # 如果是具体某个 ID 的操作（delete/patch），不走这里
            qs = qs.filter(parent=None)
        
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
        comment = serializer.save(author=self.request.user, parent=parent)
        self._send_comment_notification(comment, parent)

    def _send_comment_notification(self, comment, parent):
        """评论/回复创建后向帖子作者或被回复的评论作者发送通知。"""
        from users.models import Notification
        actor = comment.author
        post = comment.post
        if parent is not None:
            # 回复通知：通知被回复评论的作者
            recipient = parent.author
            if recipient == actor:
                return
            title = f'{actor.username} 回复了你的评论'
            content = f'在帖子《{post.title}》中："{comment.text[:50]}"'
            ntype = Notification.TYPE_REPLY
        else:
            # 评论通知：通知帖子作者
            recipient = post.author
            if recipient == actor:
                return
            title = f'{actor.username} 评论了你的帖子'
            content = f'在帖子《{post.title}》中："{comment.text[:50]}"'
            ntype = Notification.TYPE_REPLY
        Notification.objects.create(
            user=recipient,
            title=title,
            content=content,
            notification_type=ntype,
            triggered_by=actor,
        )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        user = request.user
        from users.models import User
        is_superadmin = hasattr(user, 'role') and user.role == User.ROLE_SUPERADMIN
        if comment.author != user and not is_superadmin:
            return Response({'detail': '无权删除他人评论。'}, status=status.HTTP_403_FORBIDDEN)
        # 一级评论删除时，Django CASCADE 会自动删除其所有二级回复
        print(f"[DEBUG-Delete] User {user.username} deleting comment {comment.id}")
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        评论点赞
        POST /api/forum/comments/{id}/like/
        """
        comment = self.get_object()
        like, created = CommentLike.objects.get_or_create(
            user=request.user,
            comment=comment
        )
        if created:
            comment.likes += 1
            comment.save(update_fields=['likes'])
            print(f"[DEBUG-CommentLike] New like created, total likes: {comment.likes}")
            # 通知评论作者（不通知自己）
            if comment.author != request.user:
                from users.models import Notification
                Notification.objects.create(
                    user=comment.author,
                    title=f'{request.user.username} 赞了你的评论',
                    content=f'你在帖子《{comment.post.title}》中的评论获得了一个新的点赞',
                    notification_type=Notification.TYPE_LIKE,
                    triggered_by=request.user,
                )
        else:
            print(f"[DEBUG-CommentLike] Like already exists")
        return Response({'likes': comment.likes, 'is_liked': True})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        评论取消点赞
        POST /api/forum/comments/{id}/unlike/
        """
        comment = self.get_object()
        try:
            like = CommentLike.objects.get(
                user=request.user,
                comment=comment
            )
            like.delete()
            comment.likes = max(0, comment.likes - 1)
            comment.save(update_fields=['likes'])
            print(f"[DEBUG-CommentUnlike] Like removed, total likes: {comment.likes}")
        except CommentLike.DoesNotExist:
            print(f"[DEBUG-CommentUnlike] Like not found")
            pass
        return Response({'likes': comment.likes, 'is_liked': False})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def report(self, request, pk=None):
        """
        举报评论
        POST /api/forum/comments/{id}/report/
        body: {"reason": "举报原因"}
        """
        comment = self.get_object()
        reason = request.data.get('reason', '')
        print(f"[DEBUG-CommentReport] User {request.user.username} reporting comment {comment.id}")
        
        report = CommentReport.objects.create(
            comment=comment,
            reported_by=request.user,
            reason=reason
        )
        serializer = CommentReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        existing = comment.images.count()
        remaining = 5 - existing
        if remaining <= 0:
            return Response({'detail': '已达到5张上限。'}, status=status.HTTP_400_BAD_REQUEST)
        for idx, f in enumerate(files[:remaining]):
            CommentImage.objects.create(comment=comment, image=f, sort_order=existing + idx)
        print(f"[DEBUG-Upload] {min(len(files), remaining)} images uploaded for comment {comment.id}")
        return Response({'uploaded': min(len(files), remaining)}, status=status.HTTP_201_CREATED)
