from rest_framework import serializers
from .models import QuizQuestion


class QuizQuestionSerializer(serializers.ModelSerializer):
    """
    题库题目序列化，字段名与前端 Quiz 录入面板一一对应。
    """
    image = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestion
        fields = [
            'id', 'description', 'correct_answer',
            'distractor_a', 'distractor_b',
            'image', 'monument',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class QuizQuestionWriteSerializer(serializers.ModelSerializer):
    """写入专用序列化（接受 image 文件上传）。"""

    class Meta:
        model = QuizQuestion
        fields = [
            'description', 'correct_answer',
            'distractor_a', 'distractor_b',
            'image', 'monument',
        ]
