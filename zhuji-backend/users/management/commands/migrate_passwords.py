"""
批量迁移所有用户密码到 SHA-256 兼容格式。

原理：无法从 PBKDF2 哈希逆推明文，所以此命令适用于开发/测试环境，
将所有用户密码统一重置为 SHA-256(原用户名) 作为临时密码，
然后通知用户通过"忘记密码"流程设置新密码。

生产环境建议：直接通知用户使用"忘记密码"功能重置密码。
"""
import hashlib

from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = '批量迁移所有用户密码为 SHA-256 兼容格式。每个用户的临时密码 = 其用户名。'

    def add_arguments(self, parser):
        parser.add_argument(
            '--default-password',
            type=str,
            default=None,
            help='所有用户统一重置为此明文密码（默认使用各自用户名）',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='仅打印将被影响的用户，不实际修改',
        )

    def handle(self, *args, **options):
        default_pw = options['default_password']
        dry_run = options['dry_run']
        users = User.objects.all()

        self.stdout.write(f'共 {users.count()} 个用户将被处理。')

        if dry_run:
            for u in users:
                self.stdout.write(f'  [DRY RUN] {u.username} (id={u.id})')
            return

        count = 0
        for u in users:
            plain = default_pw if default_pw else u.username
            sha256_hash = hashlib.sha256(plain.encode('utf-8')).hexdigest()
            u.set_password(sha256_hash)
            u.save(update_fields=['password'])
            count += 1
            self.stdout.write(f'  ✓ {u.username} → 临时密码: {plain}')

        self.stdout.write(self.style.SUCCESS(f'\n已重置 {count} 个用户密码。请通知用户修改密码。'))
