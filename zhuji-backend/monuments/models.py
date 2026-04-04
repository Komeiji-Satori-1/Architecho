from django.conf import settings
from django.db import models


class Monument(models.Model):
    """
    古建筑标准条目 — 对应 StampDiscovery.vue buildings 档案卡及 Modal 详情。

    字段映射：
      name           → building.name    ("佛光寺东大殿")
      location       → building.location ("山西 · 五台山")
      dynasty        → 朝代（用于筛选）
      era            → building.era     ("唐大中十一年 (857年)")
      structure_type → building.type    ("殿堂式木构")
      cover_image    → building.image
      desc           → building.desc    (短摘要，卡片展示)
      full_desc      → building.fullDesc (Modal 详细描述)

    注意：building.status（进行中/已解锁/未开始）是 per-user 状态，
    存储于 UserMonumentProgress，不在本模型中。
    """

    name = models.CharField(max_length=200, verbose_name='名称')
    location = models.CharField(max_length=200, blank=True, verbose_name='地理位置')
    dynasty = models.CharField(max_length=100, blank=True, verbose_name='朝代')
    era = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='建造年代',
        help_text='如：唐大中十一年 (857年)',
    )
    structure_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='结构类型',
        help_text='如：殿堂式木构、楼阁式木塔、重檐庑殿顶',
    )
    cover_image = models.ImageField(
        upload_to='monuments/covers/',
        blank=True,
        null=True,
        verbose_name='封面图',
    )
    desc = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='简介摘要',
        help_text='用于卡片简短展示，对应 building.desc',
    )
    full_desc = models.TextField(
        blank=True,
        verbose_name='详细描述',
        help_text='用于 Modal 档案详情，对应 building.fullDesc',
    )
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'monuments_monument'
        ordering = ['-created_at']
        verbose_name = '古建条目'
        verbose_name_plural = '古建条目列表'

    def __str__(self):
        return self.name


class UserMonumentProgress(models.Model):
    """
    用户-古建筑探索进度（per-user 状态）。

    对应 StampDiscovery.vue buildings[].status：
      '进行中' → STATUS_IN_PROGRESS
      '已解锁' → STATUS_COMPLETED
      '未开始' → STATUS_PENDING

    同时支撑 UserProfile.vue footprintStats 分类统计：
      category_type 记录该古建的分类（宫廷/园林/民居）
    """

    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, '未开始'),
        (STATUS_IN_PROGRESS, '进行中'),
        (STATUS_COMPLETED, '已解锁'),
    ]

    # UserProfile.footprintStats 分类统计
    CATEGORY_PALACE = 'palace'
    CATEGORY_GARDEN = 'garden'
    CATEGORY_FOLK = 'folk'
    CATEGORY_OTHER = 'other'

    CATEGORY_CHOICES = [
        (CATEGORY_PALACE, '宫廷建筑'),
        (CATEGORY_GARDEN, '园林景观'),
        (CATEGORY_FOLK, '民居建筑'),
        (CATEGORY_OTHER, '其他'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='monument_progresses',
        verbose_name='用户',
    )
    monument = models.ForeignKey(
        Monument,
        on_delete=models.CASCADE,
        related_name='user_progresses',
        verbose_name='古建',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='探索状态',
        db_index=True,
    )
    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_OTHER,
        verbose_name='建筑分类',
        help_text='用于 UserProfile 足迹分类统计',
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    class Meta:
        db_table = 'monuments_user_progress'
        unique_together = ('user', 'monument')
        verbose_name = '用户探索进度'
        verbose_name_plural = '用户探索进度'

    def __str__(self):
        return f'{self.user.username} → {self.monument.name} ({self.get_status_display()})'


class ArticleSubmission(models.Model):
    """
    用户投稿文章审核 — 对应 AdminDashboard.vue auditItems。

    字段完全对齐前端 auditItems 结构：
      id, title, author ("@用户名"), time ("HH:MM"),
      status ('待处理'|'已通过'|'已驳回'), image, desc

    附加字段：
      feedback  → 审核反馈建议（前端输入框 "输入审核反馈建议..."）
      monument  → 可选关联至正式古建条目
    """

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, '待处理'),
        (STATUS_APPROVED, '已通过'),
        (STATUS_REJECTED, '已驳回'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='article_submissions',
        verbose_name='投稿人',
    )
    desc = models.TextField(verbose_name='正文摘要')
    image = models.ImageField(
        upload_to='submissions/',
        blank=True,
        null=True,
        verbose_name='配图',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='审核状态',
        db_index=True,
    )
    # time 字段前端展示格式 "HH:MM"，serializer 负责格式化
    time = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    feedback = models.TextField(
        blank=True,
        verbose_name='审核反馈建议',
        help_text='对应前端"输入审核反馈建议..."输入框',
    )
    monument = models.ForeignKey(
        Monument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='article_submissions',
        verbose_name='关联古建',
    )

    class Meta:
        db_table = 'monuments_article_submission'
        ordering = ['-time']
        verbose_name = '投稿文章'
        verbose_name_plural = '投稿文章列表'

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'
