from rest_framework import serializers
from .models import ForumCategory, ForumPost, Comment,PostImage


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

    class Meta:
        model = ForumPost
        fields = [
            'id', 'title', 'excerpt', 'cover',
            'author', 'author_avatar', 'category_name',
            'is_top', 'is_essence', 'views', 'likes',
            'time', 'last_edit', 'comment_count',
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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    time = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_avatar', 'text', 'likes', 'time', 'replies']

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        if obj.author.avatar and request:
            return request.build_absolute_uri(obj.author.avatar.url)
        return None

    def get_replies(self, obj):
        if obj.parent is not None:
            return []
        children = obj.replies.select_related('author').order_by('created_at')
        return CommentSerializer(children, many=True, context=self.context).data
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
    class Meta:
        model = ForumPost
        fields = [
            'id', 'title', 'content', 'excerpt', 'cover','images',
            'author', 'author_avatar', 'category',
            'is_top', 'is_essence', 'views', 'likes',
            'time', 'last_edit', 'comment_count',
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
                # build_absolute_uri 会自动拼接 http://domain.com/media/path/to/img.jpg
                urls.append(request.build_absolute_uri(img_obj.image.url))
        return urls