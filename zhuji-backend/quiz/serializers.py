from rest_framework import serializers
from .models import QuizQuestion, QuizOption, UserQuizRecord


class QuizOptionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = QuizOption
        fields = ['id', 'label', 'image', 'is_correct', 'order']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class QuizOptionPlayerSerializer(serializers.ModelSerializer):
    """玩家端序列化器 — 不暴露 is_correct"""
    image = serializers.SerializerMethodField()

    class Meta:
        model = QuizOption
        fields = ['id', 'label', 'image', 'order']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class QuizQuestionSerializer(serializers.ModelSerializer):
    """管理端完整序列化器"""
    image = serializers.SerializerMethodField()
    options = QuizOptionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = [
            'id', 'description', 'question_type',
            'image', 'monument', 'article_page',
            'points', 'options',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class QuizQuestionPlayerSerializer(serializers.ModelSerializer):
    """玩家端序列化器 — 不暴露正确答案"""
    image = serializers.SerializerMethodField()
    options = QuizOptionPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = [
            'id', 'description', 'question_type',
            'image', 'monument', 'article_page',
            'points', 'options',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class QuizQuestionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = [
            'description', 'question_type',
            'image', 'monument', 'article_page', 'points',
        ]


class QuizOptionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = ['id', 'question', 'label', 'image', 'is_correct', 'order']
        read_only_fields = ['id']


class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
    )
