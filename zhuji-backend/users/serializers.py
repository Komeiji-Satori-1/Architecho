from rest_framework import serializers
from .models import User

# 前端 roleBg 颜色映射（role → Tailwind class）
ROLE_BG_MAP = {
    User.ROLE_SUPERADMIN: 'bg-primary/10 text-primary',
    User.ROLE_MODERATOR: 'bg-tertiary/10 text-tertiary',
    User.ROLE_USER: 'bg-secondary/10 text-secondary',
}


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
