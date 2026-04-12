from django.contrib.auth import authenticate
from django.db.models import F, Value, FloatField, Count, ExpressionWrapper
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes as perm_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserListSerializer, UserDetailSerializer, UserProfileSerializer


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
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)
class RegisterView(APIView):
    """注册接口：POST /api/users/register/"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
        password_confirm = request.data.get('password_confirm', '')

        if not username or not password:
            return Response({'detail': '请填写账号和密码。'}, status=status.HTTP_400_BAD_REQUEST)
        if password != password_confirm:
            return Response({'detail': '两次密码输入不一致。'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'detail': '该账号已被注册。'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 6:
            return Response({'detail': '密码长度不能少于6位。'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'avatar': None,
                'role': user.role,
                'level_title': user.level_title,
            },
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@perm_classes([permissions.AllowAny])
def leaderboard(request):
    """
    活跃榜：按影响力(帖子数*3 + 点赞数*1 + 答题正确数*2)降序取前 10。
    GET /api/users/leaderboard/
    """
    users = (
        User.objects
        .filter(is_active=True, role=User.ROLE_USER)
        .annotate(
            post_cnt=Count('forum_posts'),
            power=ExpressionWrapper(
                F('post_cnt') * 3 + F('quiz_correct_count') * 2,
                output_field=FloatField(),
            ),
        )
        .order_by('-power')[:10]
    )
    result = []
    for u in users:
        avatar = None
        if u.avatar and request:
            avatar = request.build_absolute_uri(u.avatar.url)
        result.append({
            'id': u.id,
            'name': u.username,
            'power': f'{u.power:.0f}' if u.power >= 1000 else f'{u.power:.0f}',
            'avatar': avatar or f'https://picsum.photos/seed/u{u.id}/100/100',
            'badges': min(u.level_num, 5),
        })
    return Response(result)