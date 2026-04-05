from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserListSerializer, UserDetailSerializer


class IsAdminOrModerator(permissions.BasePermission):
    """仅超级管理员和版主可操作用户管理接口。"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in (User.ROLE_SUPERADMIN, User.ROLE_MODERATOR)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理 ViewSet。
    - list/retrieve：返回 userList 所需结构
    - ban / unban：封禁/解封操作（对应前端"封禁/解封"按钮）
    - set_role：变更用户角色权限
    """
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsAdminOrModerator]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserListSerializer
        return UserDetailSerializer

    @action(detail=True, methods=['post'], url_path='ban')
    def ban(self, request, pk=None):
        """封禁用户：将 is_active 置为 False。"""
        user = self.get_object()
        if user.role == User.ROLE_SUPERADMIN:
            return Response(
                {'detail': '不能封禁超级管理员。'},
                status=status.HTTP_403_FORBIDDEN,
            )
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response({'detail': '用户已封禁。'})

    @action(detail=True, methods=['post'], url_path='unban')
    def unban(self, request, pk=None):
        """解封用户：将 is_active 置为 True。"""
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=['is_active'])
        return Response({'detail': '用户已解封。'})

    @action(detail=True, methods=['post'], url_path='set-role')
    def set_role(self, request, pk=None):
        """变更角色：payload { role: 'moderator' }。"""
        user = self.get_object()
        new_role = request.data.get('role')
        valid_roles = [r[0] for r in User.ROLE_CHOICES]
        if new_role not in valid_roles:
            return Response(
                {'detail': f'无效角色，可选值：{valid_roles}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.role = new_role
        user.save(update_fields=['role'])
        serializer = UserDetailSerializer(user, context={'request': request})
        return Response(serializer.data)


class LoginView(APIView):
    """登录接口：POST /api/users/login/ → 返回 JWT access + refresh token。"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return Response(
                {'detail': '请填写账号和密码。'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': '账号或密码错误。'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not user.is_active:
            return Response(
                {'detail': '账号已被封禁，请联系管理员。'},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'avatar': request.build_absolute_uri(user.avatar.url) if user.avatar else None,
                'role': user.role,
                'level_title': user.level_title,
            },
        })


class MeView(APIView):
    """当前用户信息：GET /api/users/me/ → 验证 Token 并返回用户资料。"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'avatar': request.build_absolute_uri(user.avatar.url) if user.avatar else None,
            'role': user.role,
            'level_title': user.level_title,
            'level_num': user.level_num,
            'influence_power': user.influence_power,
        })
