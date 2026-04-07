from django.conf import settings
from django.db import models


class Stamp(models.Model):
    """
    印章定义 — 同时对应两个前端场景：

    1. UserProfile.vue stamps（印章册网格）：
       id, name ("故宫 · 角楼"), image, unlocked→UserStamp.unlocked_layers>0

    2. StampDiscovery.vue 套色印章展示：
       关联 monument（学习路径），套色层由 StampColorLayer 定义

    StampLayer.vue 组件 props：
       title=stamp.name, progress=UserStamp.progress_percent,
       collected=UserStamp.unlocked_layers, total=stamp.total_layers
    """

    name = models.CharField(max_length=100, verbose_name='印章名称')
    image = models.ImageField(
        upload_to='stamps/',
        blank=True,
        null=True,
        verbose_name='印章图片',
        help_text='UserProfile 印章册中显示。未上传时展示 LockIcon',
    )
    monument = models.ForeignKey(
        'monuments.Monument',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stamps',
        verbose_name='关联古建',
        help_text='该印章隶属的古建学习路径',
    )
    total_layers = models.PositiveSmallIntegerField(
        default=3,
        verbose_name='套色层数',
        help_text='StampDiscovery 套色步骤总数，默认3层：素胎底框→朱砂描红→琉璃缀金',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stamps_stamp'
        verbose_name = '印章'
        verbose_name_plural = '印章列表'

    def __str__(self):
        return self.name


class StampColorLayer(models.Model):
    """
    印章套色层定义 — 对应 StampDiscovery.vue stampSteps[]。

    每层对应一个独立的 SVG 文件，前端按 layer_index 顺序叠加渲染。
    支持 3-5 层，使用 mix-blend-mode 控制叠加效果。

    字段映射：
      layer_index → 层级序号（1/2/3...），对应 unlockedLayers 判断
      layer_name  → step.name  ("第一层：素胎底框")
      color       → step.color ('#e2e2e2')
      svg_file    → SVG 图片文件
      blend_mode  → CSS mix-blend-mode 值
    """

    BLEND_CHOICES = [
        ('normal', 'Normal'),
        ('multiply', 'Multiply（宣纸晕染）'),
        ('screen', 'Screen'),
        ('overlay', 'Overlay'),
        ('darken', 'Darken'),
        ('color-burn', 'Color Burn'),
    ]

    stamp = models.ForeignKey(
        Stamp,
        on_delete=models.CASCADE,
        related_name='color_layers',
        verbose_name='所属印章',
    )
    layer_index = models.PositiveSmallIntegerField(
        verbose_name='层级序号',
        help_text='1=第一层，2=第二层，3=第三层…最多5层',
    )
    layer_name = models.CharField(
        max_length=100,
        verbose_name='层名称',
        help_text='如：第一层：素胎底框',
    )
    color = models.CharField(
        max_length=20,
        verbose_name='颜色值',
        help_text='十六进制颜色，如 #e2e2e2',
    )
    svg_file = models.FileField(
        upload_to='stamps/layers/',
        blank=True,
        null=True,
        verbose_name='SVG 图层文件',
        help_text='上传独立的 SVG 文件，前端按顺序叠加渲染',
    )
    blend_mode = models.CharField(
        max_length=20,
        choices=BLEND_CHOICES,
        default='multiply',
        verbose_name='混合模式',
        help_text='CSS mix-blend-mode，控制图层叠加效果',
    )

    class Meta:
        db_table = 'stamps_color_layer'
        unique_together = ('stamp', 'layer_index')
        ordering = ['layer_index']
        verbose_name = '套色层'
        verbose_name_plural = '套色层列表'

    def __str__(self):
        return f'{self.stamp.name} - {self.layer_name}'


class UserStamp(models.Model):
    """
    用户印章收藏（M2M through table）— 连接 User 与 Stamp。

    字段映射：
      unlocked_layers  → StampDiscovery.unlockedLayers（当前已解锁层数，0–total_layers）
      unlocked(属性)   → stamp.unlocked = unlocked_layers > 0（UserProfile 印章册展示）

    StampLayer.vue 组件完整 props 推导：
      title      = stamp.name
      progress   = (unlocked_layers / stamp.total_layers) * 100
      collected  = unlocked_layers
      total      = stamp.total_layers
      description= "距离解锁"xxx"称号还需收集 N 枚印记..."

    解锁触发：答对 quiz 题目后 unlocked_layers += 1（配合 UserQuizRecord）
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_stamps',
        verbose_name='用户',
    )
    stamp = models.ForeignKey(
        Stamp,
        on_delete=models.CASCADE,
        related_name='collectors',
        verbose_name='印章',
    )
    unlocked_layers = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='已解锁套色层数',
        help_text='0=未收集，>0=已收集至少一层，=total_layers=完整印记',
    )
    collected_at = models.DateTimeField(auto_now_add=True, verbose_name='首次收集时间')

    class Meta:
        db_table = 'stamps_user_stamp'
        unique_together = ('user', 'stamp')
        verbose_name = '用户印章'
        verbose_name_plural = '用户印章册'

    def __str__(self):
        return f'{self.user.username} → {self.stamp.name} ({self.unlocked_layers}/{self.stamp.total_layers}层)'

    @property
    def unlocked(self) -> bool:
        """前端 stamp.unlocked 字段：unlocked_layers > 0 即视为已收集。"""
        return self.unlocked_layers > 0

    @property
    def progress(self) -> int:
        """StampLayer.vue :progress prop，0–100。"""
        if self.stamp.total_layers == 0:
            return 0
        return round(self.unlocked_layers / self.stamp.total_layers * 100)
