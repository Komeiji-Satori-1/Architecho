from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F, Value, FloatField, Count, ExpressionWrapper
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes as perm_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import hashlib
import secrets
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
    """登录接口：POST /api/users/login/ → 返回 JWT access + refresh token。
    前端传入的是 SHA-256(password) 哈希值，后端用它作为密码进行认证。
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # 跳过 SessionAuthentication 避免 CSRF

    def post(self, request):
        username = request.data.get('username', '').strip()
        password_hash = request.data.get('password', '')

        if not username or not password_hash:
            return Response(
                {'detail': '请填写账号和密码。'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password_hash)
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
    """注册接口：POST /api/users/register/
    前端传入的是 SHA-256(password) 哈希值。
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # 跳过 SessionAuthentication 避免 CSRF

    def post(self, request):
        username = request.data.get('username', '').strip()
        password_hash = request.data.get('password', '')
        password_confirm = request.data.get('password_confirm', '')
        email = request.data.get('email', '').strip()

        if not username or not password_hash:
            return Response({'detail': '请填写账号和密码。'}, status=status.HTTP_400_BAD_REQUEST)
        if password_hash != password_confirm:
            return Response({'detail': '两次密码输入不一致。'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'detail': '该账号已被注册。'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password_hash) < 6:
            return Response({'detail': '密码长度不能少于6位。'}, status=status.HTTP_400_BAD_REQUEST)
        if email and User.objects.filter(email=email).exists():
            return Response({'detail': '该邮箱已被注册。'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password_hash)
        if email:
            user.email = email
            user.save(update_fields=['email'])
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


class ForgotPasswordRequestView(APIView):
    """忘记密码 - 第一步：发送验证码到邮箱。
    POST /api/users/forgot-password/request/
    body: { email }
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email', '').strip()
        if not email:
            return Response({'detail': '请填写邮箱地址。'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'detail': '该邮箱未注册。'}, status=status.HTTP_404_NOT_FOUND)

        # 生成 6 位随机验证码，存入缓存，10 分钟过期
        code = f'{secrets.randbelow(1000000):06d}'
        cache_key = f'pwd_reset:{email}'
        cache.set(cache_key, code, timeout=600)  # 10分钟

        try:
            send_mail(
                subject='【筑迹】密码重置验证码',
                message=f'您的密码重置验证码为：{code}\n\n该验证码 10 分钟内有效，请勿泄露给他人。',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            return Response({'detail': '邮件发送失败，请稍后重试。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': '验证码已发送至您的邮箱。'})


class ForgotPasswordResetView(APIView):
    """忘记密码 - 第二步：验证码 + 新密码。
    POST /api/users/forgot-password/reset/
    body: { email, code, new_password }
    new_password 是前端 SHA-256 哈希后的值。
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email', '').strip()
        code = request.data.get('code', '').strip()
        new_password_hash = request.data.get('new_password', '')

        if not email or not code or not new_password_hash:
            return Response({'detail': '请填写完整信息。'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'pwd_reset:{email}'
        cached_code = cache.get(cache_key)

        if cached_code is None:
            return Response({'detail': '验证码已过期，请重新获取。'}, status=status.HTTP_400_BAD_REQUEST)
        if cached_code != code:
            return Response({'detail': '验证码错误。'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'detail': '用户不存在。'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password_hash)
        user.save(update_fields=['password'])
        cache.delete(cache_key)  # 用后即删

        return Response({'detail': '密码重置成功，请重新登录。'})


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