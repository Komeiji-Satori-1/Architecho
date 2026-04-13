from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from monuments.models import ArticleSubmission
from users.models import User

from .models import SensitiveWord, AIConfig, AIInterceptionLog, NodeStatus
from .serializers import (
    SensitiveWordSerializer,
    AIConfigSerializer,
    NodeStatusSerializer,
    DashboardStatsSerializer,
)


class IsAdminUser(permissions.BasePermission):
    """仅超级管理员或版主可访问系统配置接口。"""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in (User.ROLE_SUPERADMIN, User.ROLE_MODERATOR)
        )


class DashboardStatsView(APIView):
    """
    统计大盘聚合接口 GET /api/system/dashboard/
    返回对应前端 stats 数组所需的实时汇总数据：
      - today_submissions : 今日新增投稿数
      - pending_audit     : 待审核任务数
      - active_users      : 活跃（未封禁）用户数
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.now().date()

        today_submissions = ArticleSubmission.objects.filter(
            time__date=today
        ).count()

        pending_audit = ArticleSubmission.objects.filter(
            status=ArticleSubmission.STATUS_PENDING
        ).count()

        active_users = User.objects.filter(is_active=True).count()

        data = {
            'today_submissions': today_submissions,
            'pending_audit': pending_audit,
            'active_users': active_users,
        }
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)


class SensitiveWordViewSet(viewsets.ModelViewSet):
    """
    敏感词库 CRUD。
    对应前端 keywords 芯片列表（增删查）。
    """
    queryset = SensitiveWord.objects.all()
    serializer_class = SensitiveWordSerializer
    permission_classes = [IsAdminUser]


class AIConfigViewSet(viewsets.ModelViewSet):
    """
    AI 监管配置（单例）。
    前端通过 PATCH /api/system/ai-config/1/ 提交拦截强度。
    """
    queryset = AIConfig.objects.all()
    serializer_class = AIConfigSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'patch', 'head', 'options']

    @action(detail=False, methods=['get'], url_path='current')
    def current(self, request):
        """获取当前唯一配置项，若不存在则自动初始化。"""
        config, _ = AIConfig.objects.get_or_create(pk=1)
        return Response(AIConfigSerializer(config).data)


class NodeStatusViewSet(viewsets.ModelViewSet):
    """
    系统节点负载数据。
    可通过 POST 写入采集数据（对接自动化监控脚本）。
    """
    queryset = NodeStatus.objects.all()
    serializer_class = NodeStatusSerializer
    permission_classes = [IsAdminUser]
