from rest_framework import serializers
from .models import Monument, ArticleSubmission


class MonumentSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Monument
        fields = [
            'id', 'name', 'location', 'dynasty', 'era',
            'structure_type', 'cover_image', 'desc', 'full_desc',
            'is_published', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None


class SubmissionListSerializer(serializers.ModelSerializer):
    """
    适配前端 auditItems 常量结构：
    { id, title, author, time, status, image, desc }
    """
    # 前端 author 为 "@用户名" 格式
    author = serializers.SerializerMethodField()
    # 前端 time 仅展示 HH:MM
    time = serializers.DateTimeField(format='%H:%M', read_only=True)
    # 前端 status 展示中文
    status = serializers.CharField(source='get_status_display', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = ArticleSubmission
        fields = ['id', 'title', 'author', 'time', 'status', 'image', 'desc']

    def get_author(self, obj):
        return f'@{obj.author.username}'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class SubmissionDetailSerializer(serializers.ModelSerializer):
    """审核端完整投稿详情（含写入字段）。"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = ArticleSubmission
        fields = [
            'id', 'title', 'author', 'author_name', 'desc',
            'image', 'status', 'status_display', 'time',
            'feedback', 'monument',
        ]
        read_only_fields = ['id', 'author', 'author_name', 'time', 'status_display']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class SubmissionAuditSerializer(serializers.Serializer):
    """审核操作专用：接收 status 和 feedback 字段。"""
    status = serializers.ChoiceField(choices=[
        ArticleSubmission.STATUS_APPROVED,
        ArticleSubmission.STATUS_REJECTED,
    ])
    feedback = serializers.CharField(allow_blank=True, default='')
