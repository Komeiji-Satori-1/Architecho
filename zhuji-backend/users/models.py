from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型。字段完全对齐前端各页面数据结构：

    AdminDashboard.userList:
      name → username, email, role, roleBg(computed), active→is_active, avatar

    UserProfile:
      level_num + level_title → "二级 · 营造生"
      influence_power         → 活跃榜 power "9.8k"
      quiz_correct_count/quiz_total_count → 答题正确率 89%
      footprint_count         → 探索足迹 42/150
    """

    ROLE_SUPERADMIN = 'superadmin'
    ROLE_MODERATOR = 'moderator'
    ROLE_USER = 'user'

    ROLE_CHOICES = [
        (ROLE_SUPERADMIN, '超级管理员'),
        (ROLE_MODERATOR, '版主'),
        (ROLE_USER, '普通用户'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
        verbose_name='角色',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='头像',
    )
    bio = models.TextField(blank=True, verbose_name='个人简介')

    # ---- UserProfile: 等级系统 ----
    # sidbar: "二级 · 营造生"
    level_num = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='等级数字',
        help_text='对应 UserProfile 侧边栏 "二级·营造生" 中的数字',
    )
    level_title = models.CharField(
        max_length=50,
        default='入门学徒',
        verbose_name='等级称号',
        help_text='如：营造生、营造师、大匠',
    )

    # ---- ForumList.topUsers: 影响力 ----
    # 活跃榜 power "9.8k"
    influence_power = models.PositiveIntegerField(
        default=0,
        verbose_name='影响力值',
    )

    # ---- UserProfile: 答题正确率 ----
    # Dashboard: "89% 正确 / 在 240 个知识点中领先 92%"
    quiz_correct_count = models.PositiveIntegerField(
        default=0,
        verbose_name='答题正确数',
    )
    quiz_total_count = models.PositiveIntegerField(
        default=0,
        verbose_name='答题总数',
    )

    # ---- UserProfile: 探索足迹 ----
    # "42/150 古建筑考察 · 遍及14省市"
    footprint_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='已探索古建数',
    )

    class Meta:
        db_table = 'users_user'
        verbose_name = '用户'
        verbose_name_plural = '用户列表'

    @property
    def name(self) -> str:
        """前端 userList.name：优先全名，否则用户名。"""
        full = self.get_full_name()
        return full if full else self.username

    @property
    def active(self) -> bool:
        """前端 userList.active → is_active。"""
        return self.is_active

    @property
    def quiz_accuracy(self) -> float:
        """答题正确率百分比，对应 UserProfile Dashboard 89%。"""
        if self.quiz_total_count == 0:
            return 0.0
        return round(self.quiz_correct_count / self.quiz_total_count * 100, 1)

    @property
    def level_label(self) -> str:
        """完整等级标签，如 '二级 · 营造生'，对应前端侧边栏展示。"""
        return f'{self.level_num}级 · {self.level_title}'


class Notification(models.Model):
    """
    用户通知消息 — 对应 UserProfile.vue messages 列表。

    字段映射：
      title        → msg.title
      content      → msg.content
      unread       → msg.unread（未读红点）
      notification_type → msg.typeBg / msg.typeColor / msg.icon（前端根据 type 动态渲染）
      triggered_by → 触发通知的用户（如"李工回复了你"中的李工）
      created_at   → msg.time（serializer 输出相对时间）
    """

    TYPE_REPLY = 'reply'            # 回复（MessageIcon, bg-primary/5）
    TYPE_ANNOUNCEMENT = 'announcement'  # 官方公告（InfoIcon, bg-tertiary/5）
    TYPE_BADGE = 'badge'            # 获得勋章（StarIcon, bg-on-surface/5）
    TYPE_REWARD = 'reward'          # 奖励（GiftIcon）

    TYPE_CHOICES = [
        (TYPE_REPLY, '回复通知'),
        (TYPE_ANNOUNCEMENT, '官方公告'),
        (TYPE_BADGE, '勋章通知'),
        (TYPE_REWARD, '奖励通知'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='接收用户',
    )
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_ANNOUNCEMENT,
        verbose_name='通知类型',
    )
    unread = models.BooleanField(default=True, verbose_name='是否未读', db_index=True)
    # 触发通知的操作用户（如谁回复了我）
    triggered_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='triggered_notifications',
        verbose_name='触发用户',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间', db_index=True)

    class Meta:
        db_table = 'users_notification'
        ordering = ['-created_at']
        verbose_name = '通知消息'
        verbose_name_plural = '通知消息列表'

    def __str__(self):
        return f'[{self.get_notification_type_display()}] {self.title}'


class Reward(models.Model):
    """
    用户奖励 — 对应 UserProfile.vue rewards 列表。

    字段映射：
      name       → reward.name  (如 "故宫门票优惠券")
      desc       → reward.desc  (如 "有效期至 2026-12-31")
      reward_type → reward.icon 的选择依据（coupon→TicketIcon / badge→AwardIcon）
      expires_at → 优惠券类奖励的有效期
    """

    TYPE_COUPON = 'coupon'   # 优惠券 → TicketIcon
    TYPE_BADGE = 'badge'     # 专属勋章 → AwardIcon
    TYPE_OTHER = 'other'

    TYPE_CHOICES = [
        (TYPE_COUPON, '优惠券'),
        (TYPE_BADGE, '专属勋章'),
        (TYPE_OTHER, '其他奖励'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='rewards',
        verbose_name='用户',
    )
    name = models.CharField(max_length=100, verbose_name='奖励名称')
    desc = models.CharField(max_length=200, verbose_name='描述')
    reward_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_OTHER,
        verbose_name='奖励类型',
    )
    expires_at = models.DateField(
        null=True,
        blank=True,
        verbose_name='有效期',
        help_text='仅优惠券类奖励需填写',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发放时间')

    class Meta:
        db_table = 'users_reward'
        ordering = ['-created_at']
        verbose_name = '用户奖励'
        verbose_name_plural = '用户奖励列表'

    def __str__(self):
        return f'{self.user.username} - {self.name}'
