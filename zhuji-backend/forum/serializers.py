from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import (
    ForumCategory, ForumPost, Comment, PostImage, CommentImage,
    ForumInteraction, CommentLike, PostReport, CommentReport
)


class ForumCategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ForumCategory
        fields = ['id', 'name', 'hot', 'sort_order', 'post_count']


class ForumPostCreateSerializer(serializers.ModelSerializer):
    """发布新帖：POST /api/forum/posts/"""

    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'content', 'excerpt', 'category', 'cover']
        extra_kwargs = {
            'excerpt': {'required': False, 'allow_blank': True},
            'cover': {'required': False},
            'category': {'required': False},
        }


class ForumPostHotSerializer(serializers.ModelSerializer):
    """首页热门话题列表：title + author + reads(views)"""
    author = serializers.CharField(source='author.username', read_only=True)
    reads = serializers.IntegerField(source='views', read_only=True)

    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'author', 'reads']


class ForumPostListSerializer(serializers.ModelSerializer):
    """帖子列表卡片"""
    author = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    cover = serializers.SerializerMethodField()
    time = serializers.DateTimeField(source='created_at', format='%Y-%m-%d', read_only=True)
    last_edit = serializers.DateTimeField(source='updated_at', format='%Y-%m-%d %H:%M', read_only=True)
    heat_score = serializers.SerializerMethodField()  # 热度分数
    is_liked = serializers.SerializerMethodField()  # 当前用户是否已点赞

    class Meta:
        model = ForumPost
        fields = [
            'id', 'title', 'excerpt', 'cover',
            'author', 'author_avatar', 'category_name',
            'is_top', 'is_essence', 'views', 'likes', 'share_count',
            'time', 'last_edit', 'comment_count',
            'heat_score', 'is_liked',
        ]

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        if obj.author.avatar and request:
            return request.build_absolute_uri(obj.author.avatar.url)
        return None

    def get_cover(self, obj):
        request = self.context.get('request')
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None
    
    def get_heat_score(self, obj):
        """
        热度 = views*0.2 + likes*0.3 + comments*0.5 + 时间衰减因子
        时间衰减：超过7天的帖子热度 * 0.9^(天数-7)
        """
        base_heat = obj.views * 0.2 + obj.likes * 0.3 + obj.comment_count * 0.5
        
        # 时间衰减因子
        days_old = (timezone.now() - obj.created_at).days
        decay_factor = 0.9 ** max(0, days_old - 7)  # 7天后开始衰减
        
        final_heat = round(base_heat * decay_factor, 2)
        print(f"[DEBUG] Post {obj.id} heat calculation: views={obj.views}, likes={obj.likes}, comments={obj.comment_count}, days_old={days_old}, heat={final_heat}")
        return final_heat
    
    def get_is_liked(self, obj):
        """当前用户是否已点赞"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        is_liked = obj.interactions.filter(
            user=request.user,
            interaction_type=ForumInteraction.LIKE
        ).exists()
        print(f"[DEBUG] User {request.user.username} liked post {obj.id}: {is_liked}")
        return is_liked


class CommentImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CommentImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    time = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M', read_only=True)
    replies = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(
        queryset=ForumPost.objects.all(),
        write_only=True
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), 
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_avatar', 'text', 'likes', 'time', 'images', 'replies', 'is_liked', 'post', 'parent']

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        if obj.author.avatar and request:
            return request.build_absolute_uri(obj.author.avatar.url)
        return None

    def get_images(self, obj):
        # 只有一级评论才有图片
        if obj.parent is not None:
            return []
        imgs = obj.images.all()
        return CommentImageSerializer(imgs, many=True, context=self.context).data

    def get_replies(self, obj):
        if obj.parent is not None:
            return []
        return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
    
    def get_is_liked(self, obj):
        """当前用户是否已点赞该评论"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        is_liked = CommentLike.objects.filter(
            user=request.user,
            comment=obj
        ).exists()
        print(f"[DEBUG] User {request.user.username} liked comment {obj.id}: {is_liked}")
        return is_liked
class PostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class ForumPostDetailSerializer(serializers.ModelSerializer):
    """帖子详情页"""
    author = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name', read_only=True)
    cover = serializers.SerializerMethodField()
    time = serializers.DateTimeField(source='created_at', format='%Y-%m-%d', read_only=True)
    last_edit = serializers.DateTimeField(source='updated_at', format='%Y-%m-%d %H:%M', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    images = serializers.SerializerMethodField()
    heat_score = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = ForumPost
        fields = [
            'id', 'title', 'content', 'excerpt', 'cover', 'images',
            'author', 'author_avatar', 'category',
            'is_top', 'is_essence', 'views', 'likes', 'share_count',
            'time', 'last_edit', 'comment_count',
            'heat_score', 'is_liked',
        ]

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        if obj.author.avatar and request:
            return request.build_absolute_uri(obj.author.avatar.url)
        return None

    def get_cover(self, obj):
        request = self.context.get('request')
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None
    
    def get_images(self, obj):
        """将关联的 PostImage 对象的图片路径转换为完整 URL 数组"""
        request = self.context.get('request')
        # obj.images 来自我们在 Model 中定义的 related_name
        image_queryset = obj.images.all() 
        
        urls = []
        for img_obj in image_queryset:
            if img_obj.image and request:
                urls.append(request.build_absolute_uri(img_obj.image.url))
        return urls
    
    def get_heat_score(self, obj):
        """计算热度分数"""
        base_heat = obj.views * 0.2 + obj.likes * 0.3 + obj.comment_count * 0.5
        days_old = (timezone.now() - obj.created_at).days
        decay_factor = 0.9 ** max(0, days_old - 7)
        final_heat = round(base_heat * decay_factor, 2)
        print(f"[DEBUG-Detail] Post {obj.id} heat: {final_heat}")
        return final_heat
    
    def get_is_liked(self, obj):
        """当前用户是否已点赞"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        is_liked = obj.interactions.filter(
            user=request.user,
            interaction_type=ForumInteraction.LIKE
        ).exists()
        return is_liked


# ==================== 新增交互序列化器 ====================

class InteractionSerializer(serializers.ModelSerializer):
    """帖子交互（点赞/转发）"""
    class Meta:
        model = ForumInteraction
        fields = ['id', 'user', 'post', 'interaction_type', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    """评论点赞"""
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostReportSerializer(serializers.ModelSerializer):
    """帖子举报"""
    reported_by_username = serializers.CharField(source='reported_by.username', read_only=True)
    reviewed_by_username = serializers.CharField(source='reviewed_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = PostReport
        fields = [
            'id', 'post', 'reported_by', 'reported_by_username', 'reason',
            'status', 'created_at', 'reviewed_at', 'reviewed_by', 'reviewed_by_username'
        ]
        read_only_fields = ['id', 'created_at', 'reviewed_at', 'reviewed_by']


class CommentReportSerializer(serializers.ModelSerializer):
    """评论举报"""
    reported_by_username = serializers.CharField(source='reported_by.username', read_only=True)
    reviewed_by_username = serializers.CharField(source='reviewed_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = CommentReport
        fields = [
            'id', 'comment', 'reported_by', 'reported_by_username', 'reason',
            'status', 'created_at', 'reviewed_at', 'reviewed_by', 'reviewed_by_username'
        ]
        read_only_fields = ['id', 'created_at', 'reviewed_at', 'reviewed_by']