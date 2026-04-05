from rest_framework import serializers
from .models import ForumCategory, ForumPost, Comment


class ForumCategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ForumCategory
        fields = ['id', 'name', 'hot', 'sort_order', 'post_count']


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
    comment_count = serializers.IntegerField(source='comment_count', read_only=True)
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


class ForumPostDetailSerializer(serializers.ModelSerializer):
    """帖子详情页"""
    author = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name', read_only=True)
    cover = serializers.SerializerMethodField()
    time = serializers.DateTimeField(source='created_at', format='%Y-%m-%d', read_only=True)
    last_edit = serializers.DateTimeField(source='updated_at', format='%Y-%m-%d %H:%M', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ForumPost
        fields = [
            'id', 'title', 'content', 'excerpt', 'cover',
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
