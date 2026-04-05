from rest_framework import serializers
from .models import CoCreationItem


class CoCreationNewsSerializer(serializers.ModelSerializer):
    """
    首页「共创动态」卡片序列化器。
    返回最近已采纳的共创条目，前端据 type 字段选择图标和标签。
    """
    type = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = CoCreationItem
        fields = ['id', 'type', 'label', 'content']

    def get_type(self, obj):
        return 'adopted'

    def get_label(self, obj):
        return '官方采纳'

    def get_content(self, obj):
        return f'用户 @{obj.author.username} 提交的"{obj.title}"已被列入试产计划。'


class CoCreationListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = CoCreationItem
        fields = [
            'id', 'title', 'author', 'avatar', 'cover',
            'material', 'desc', 'featured', 'likes',
            'status', 'status_display', 'progress_percent',
        ]

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.author.avatar and request:
            return request.build_absolute_uri(obj.author.avatar.url)
        return None

    def get_cover(self, obj):
        request = self.context.get('request')
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None
