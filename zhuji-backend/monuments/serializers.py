from rest_framework import serializers
from .models import Monument, ArticleSubmission, MonumentArticle, MonumentArticlePage


class MonumentSerializer(serializers.ModelSerializer):
    has_article = serializers.SerializerMethodField()
    cover_image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Monument
        fields = [
            'id', 'name', 'location', 'dynasty', 'era',
            'structure_type', 'cover_image', 'desc', 'full_desc',
            'is_published', 'created_at', 'updated_at', 'has_article',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    def get_has_article(self, obj):
        return hasattr(obj, 'article')
class MonumentDiscoverySerializer(serializers.ModelSerializer):
    """用于 StampDiscovery 探索视窗，含用户探索进度"""
    cover_image = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    has_article = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Monument
        fields = [
            'id', 'name', 'location', 'dynasty', 'era',
            'structure_type', 'cover_image', 'desc', 'full_desc',
            'status', 'has_article', 'progress_percent',
        ]

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    def get_status(self, obj):
        user = self.context.get('request', {})
        if hasattr(user, 'user'):
            user = user.user
        else:
            return 'pending'
        progress = getattr(obj, '_user_progress', None)
        if progress:
            return progress.status
        return 'pending'

    def get_has_article(self, obj):
        return hasattr(obj, 'article')

    def get_progress_percent(self, obj):
        progress = getattr(obj, '_user_progress', None)
        if not progress:
            return 0
        if progress.status == 'completed':
            return 100
        if progress.status == 'in_progress':
            return 50
        return 0


class MonumentArticlePageSerializer(serializers.ModelSerializer):
    quiz_questions = serializers.SerializerMethodField()

    class Meta:
        model = MonumentArticlePage
        fields = ['id', 'page_number', 'content', 'quiz_questions']

    def get_quiz_questions(self, obj):
        from quiz.serializers import QuizQuestionSerializer
        qs = obj.quiz_questions.prefetch_related('options').all()
        return QuizQuestionSerializer(qs, many=True, context=self.context).data


class MonumentArticleSerializer(serializers.ModelSerializer):
    pages = MonumentArticlePageSerializer(many=True, read_only=True)
    monument_name = serializers.CharField(source='monument.name', read_only=True)

    class Meta:
        model = MonumentArticle
        fields = ['id', 'monument', 'monument_name', 'title', 'pages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MonumentArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonumentArticle
        fields = ['monument', 'title']


class MonumentArticlePageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonumentArticlePage
        fields = ['id', 'article', 'page_number', 'content']
        read_only_fields = ['id']


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
