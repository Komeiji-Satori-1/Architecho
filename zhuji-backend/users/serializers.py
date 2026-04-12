from rest_framework import serializers
from .models import User, Notification, Reward

# 前端 roleBg 颜色映射（role → Tailwind class）
ROLE_BG_MAP = {
    User.ROLE_SUPERADMIN: 'bg-primary/10 text-primary',
    User.ROLE_MODERATOR: 'bg-tertiary/10 text-tertiary',
    User.ROLE_USER: 'bg-secondary/10 text-secondary',
}


class NotificationSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    type = serializers.CharField(source='notification_type', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'content', 'type', 'unread', 'time']

    def get_time(self, obj):
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        if delta.days > 0:
            return f'{delta.days}天前'
        hours = delta.seconds // 3600
        if hours > 0:
            return f'{hours}小时前'
        minutes = delta.seconds // 60
        if minutes > 0:
            return f'{minutes}分钟前'
        return '刚刚'


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'name', 'desc', 'reward_type']


class UserProfileSerializer(serializers.ModelSerializer):
    """个人主页完整数据序列化器，供 MeView 返回。"""
    avatar = serializers.SerializerMethodField()
    level_label = serializers.CharField(read_only=True)
    quiz_accuracy = serializers.FloatField(read_only=True)
    notifications = NotificationSerializer(many=True, read_only=True)
    rewards = RewardSerializer(many=True, read_only=True)
    stamp_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    cocreation_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'avatar', 'role', 'bio',
            'level_num', 'level_title', 'level_label',
            'influence_power',
            'quiz_correct_count', 'quiz_total_count', 'quiz_accuracy',
            'footprint_count',
            'notifications', 'rewards',
            'stamp_count', 'post_count', 'cocreation_count',
        ]

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_stamp_count(self, obj):
        if hasattr(obj, 'stamp_unlocks'):
            return obj.stamp_unlocks.count()
        return 0

    def get_post_count(self, obj):
        if hasattr(obj, 'posts'):
            return obj.posts.count()
        return 0

    def get_cocreation_count(self, obj):
        if hasattr(obj, 'cocreations'):
            return obj.cocreations.count()
        return 0


class UserListSerializer(serializers.ModelSerializer):
    """
    适配前端 AdminDashboard 中 userList 常量结构：
    { id, name, email, role, roleBg, active, avatar }
    """
    name = serializers.CharField(source='username', read_only=True)
    role = serializers.SerializerMethodField()
    roleBg = serializers.SerializerMethodField()
    active = serializers.BooleanField(source='is_active', read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'roleBg', 'active', 'avatar']

    def get_role(self, obj):
        return obj.get_role_display()

    def get_roleBg(self, obj):
        return ROLE_BG_MAP.get(obj.role, 'bg-secondary/10 text-secondary')

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class UserDetailSerializer(serializers.ModelSerializer):
    """管理端完整用户信息序列化（含写入字段）。"""
    name = serializers.CharField(source='username')
    active = serializers.BooleanField(source='is_active')
    roleBg = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'role', 'roleBg',
            'active', 'avatar', 'bio', 'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']

    def get_roleBg(self, obj):
        return ROLE_BG_MAP.get(obj.role, 'bg-secondary/10 text-secondary')
