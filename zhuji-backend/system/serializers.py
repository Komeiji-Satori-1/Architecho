from rest_framework import serializers
from .models import SensitiveWord, AIConfig, AIInterceptionLog, NodeStatus


class SensitiveWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveWord
        fields = ['id', 'word', 'created_at']
        read_only_fields = ['id', 'created_at']


class AIConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConfig
        fields = ['id', 'interception_strength', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class AIInterceptionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIInterceptionLog
        fields = ['id', 'content_type', 'content_id', 'reason', 'intercepted_at']
        read_only_fields = ['id', 'intercepted_at']


class NodeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeStatus
        fields = ['id', 'node_index', 'load_percentage', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']


class DashboardStatsSerializer(serializers.Serializer):
    """
    统计大盘聚合数据序列化。
    """
    today_submissions = serializers.IntegerField()
    pending_audit = serializers.IntegerField()
    active_users = serializers.IntegerField()
