"""
一次性迁移命令：将所有现有用户的密码从 make_password(明文) 转为 make_password(SHA-256(明文))。

由于我们无法从 Django 的 PBKDF2 哈希中逆推明文密码，这个命令的做法是：
为所有用户重置密码为一个已知的默认值，然后通知用户修改密码。

或者，更好的方案：直接把现有用户密码标记为需要重置。
但最简单的过渡方案是：让后端 LoginView 同时兼容两种格式。

实际上我们可以在 LoginView 中做兼容：
1. 先用前端传来的值（SHA-256 hash）尝试认证
2. 如果失败，把传来的值当作「可能是旧的明文注册时的 SHA-256」，
   遍历检查是否是 SHA-256 格式（64位hex），如果是，则无法反推。

结论：无法自动迁移。最佳方案是在 LoginView 中添加回退逻辑 —
如果 SHA-256 hash 认证失败，尝试暴力匹配（不可行），
或者强制旧用户通过"忘记密码"流程重置。

本命令提供一个折中方案：管理员手动为指定用户重置密码。
"""
import hashlib

from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = '为指定用户重置密码（SHA-256 兼容格式）。用法: python manage.py reset_user_password <username> <new_plain_password>'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='用户名')
        parser.add_argument('plain_password', type=str, help='新的明文密码')

    def handle(self, *args, **options):
        username = options['username']
        plain_password = options['plain_password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'用户 "{username}" 不存在。'))
            return

        # 模拟前端行为：先 SHA-256，再让 Django set_password
        sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
        user.set_password(sha256_hash)
        user.save(update_fields=['password'])

        self.stdout.write(self.style.SUCCESS(
            f'用户 "{username}" 的密码已重置为 SHA-256 兼容格式。'
        ))
