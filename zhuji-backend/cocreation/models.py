from django.conf import settings
from django.db import models


class CoCreationItem(models.Model):
    """
    共创筑品条目 — 完整对应 CoCreation.vue 三种数据结构：

    1. coCreations（众创灵感瀑布流）:
       id, title, author, avatar→author.avatar, likes, image(封面), featured

    2. myProgress（创意进度侧边栏）:
       id, name→title, status('已采纳'|'待审核'), percent→progress_percent, image

    3. form（发起新创意表单）:
       name→title, material, desc
       images → CoCreationImage 关联图片

    进度步骤（前端硬编码 4 步）：
      提交(submitted) → 初审(reviewing) → 打样(sampling) → 试产(producing) → 已采纳(adopted)
    """

    # ---- 主材选择（form.material，前端 <select> 选项）----
    MATERIAL_CHOICES = [
        ('原木', '原木'),
        ('青砖', '青砖'),
        ('石材', '石材'),
        ('金属', '金属'),
    ]

    # ---- 进度状态（对应前端 4 步进度条 + 最终结果）----
    STATUS_SUBMITTED = 'submitted'   # 提交（待审核）
    STATUS_REVIEWING = 'reviewing'   # 初审中
    STATUS_SAMPLING = 'sampling'     # 打样中
    STATUS_PRODUCING = 'producing'   # 试产中
    STATUS_ADOPTED = 'adopted'       # 已采纳
    STATUS_REJECTED = 'rejected'     # 已驳回

    STATUS_CHOICES = [
        (STATUS_SUBMITTED, '待审核'),
        (STATUS_REVIEWING, '初审中'),
        (STATUS_SAMPLING, '打样中'),
        (STATUS_PRODUCING, '试产中'),
        (STATUS_ADOPTED, '已采纳'),
        (STATUS_REJECTED, '已驳回'),
    ]

    # ---- 核心字段 ----
    title = models.CharField(
        max_length=200,
        verbose_name='筑品名称',
        help_text='对应 coCreations.title 和 form.name',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cocreations',
        verbose_name='创作者',
    )
    material = models.CharField(
        max_length=20,
        choices=MATERIAL_CHOICES,
        default='原木',
        verbose_name='主材',
    )
    desc = models.TextField(
        verbose_name='创意描述',
        help_text='对应 form.desc "描述你的灵感来源与设计理念..."',
    )

    # ---- 展示字段 ----
    # 瀑布流封面图（与 CoCreationImage 的区别：cover 是主展示图，images 是灵感图集）
    cover = models.ImageField(
        upload_to='cocreation/covers/',
        blank=True,
        null=True,
        verbose_name='封面图',
        help_text='对应 coCreations.image 瀑布流展示图',
    )
    featured = models.BooleanField(
        default=False,
        verbose_name='本周精选',
        help_text='对应 coCreations.featured（"本周精选"标签）',
    )
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name='点赞数',
        help_text='对应 coCreations.likes "1.2k"',
    )

    # ---- 进度字段 ----
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SUBMITTED,
        verbose_name='进度状态',
        db_index=True,
    )
    progress_percent = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='官方反馈进度(%)',
        help_text='对应 myProgress.percent，范围 0-100，前端进度条展示',
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'cocreation_item'
        ordering = ['-created_at']
        verbose_name = '共创筑品'
        verbose_name_plural = '共创筑品列表'

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'

    @property
    def status_display_short(self) -> str:
        """前端 myProgress.status 展示值：只显示 '已采纳' 或 '待审核'。"""
        if self.status == self.STATUS_ADOPTED:
            return '已采纳'
        return '待审核'


class CoCreationImage(models.Model):
    """
    共创筑品灵感图 — 对应 CoCreation.vue form.images[]。

    前端上传逻辑：
      addImage() 添加图片，removeImage(idx) 删除
      网格展示：grid-cols-2 sm:grid-cols-4 aspect-square
    """

    item = models.ForeignKey(
        CoCreationItem,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='关联筑品',
    )
    image = models.ImageField(
        upload_to='cocreation/images/',
        verbose_name='灵感图',
    )
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'cocreation_image'
        ordering = ['sort_order']
        verbose_name = '筑品灵感图'
        verbose_name_plural = '筑品灵感图列表'

    def __str__(self):
        return f'{self.item.title} 图片 #{self.sort_order}'
