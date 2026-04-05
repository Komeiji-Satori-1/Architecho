from rest_framework import serializers
from .models import UserStamp


class StampProgressSerializer(serializers.Serializer):
    """
    首页 StampLayer 组件数据序列化器。
    输入：UserStamp 实例
    输出：{ title, progress, collected, total, description }
    """
    title = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    collected = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.stamp.name

    def get_progress(self, obj):
        total = obj.stamp.total_layers
        if total == 0:
            return 0
        return int((obj.unlocked_layers / total) * 100)

    def get_collected(self, obj):
        return obj.unlocked_layers

    def get_total(self, obj):
        return obj.stamp.total_layers

    def get_description(self, obj):
        remaining = obj.stamp.total_layers - obj.unlocked_layers
        if remaining <= 0:
            return f'恭喜！你已完全解锁「{obj.stamp.name}」印章。'
        return (
            f'距离完全解锁「{obj.stamp.name}」还需再答对 {remaining} 道题目。'
            f'每次答对均可解锁一层新的套色。'
        )
