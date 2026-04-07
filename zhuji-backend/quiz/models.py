from django.conf import settings
from django.db import models


class QuizQuestion(models.Model):
    """
    古建知识题库条目 — 对应 MonumentArticle.vue 答题组件。

    支持多种题型：
      single — 单选题（文字选项或图片选项）
      multi  — 多选题（文字选项或图片选项）

    关联关系：
      monument       → 归属古建
      article_page   → 关联文章页（阅读完本页后弹出此题）
      points         → 答对获得积分
    """

    TYPE_SINGLE = 'single'
    TYPE_MULTI = 'multi'

    TYPE_CHOICES = [
        (TYPE_SINGLE, '单选题'),
        (TYPE_MULTI, '多选题'),
    ]

    description = models.TextField(verbose_name='题目描述')
    question_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_SINGLE,
        verbose_name='题目类型',
    )
    image = models.ImageField(
        upload_to='quiz/',
        blank=True,
        null=True,
        verbose_name='题目配图',
        help_text='题干中的参考图片（可选）',
    )
    monument = models.ForeignKey(
        'monuments.Monument',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quiz_questions',
        verbose_name='关联古建',
    )
    article_page = models.ForeignKey(
        'monuments.MonumentArticlePage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quiz_questions',
        verbose_name='关联文章页',
        help_text='阅读完该页后弹出此题',
    )
    points = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='答对积分',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'quiz_question'
        ordering = ['-created_at']
        verbose_name = '题库题目'
        verbose_name_plural = '题库题目列表'

    def __str__(self):
        return self.description[:60]


class QuizOption(models.Model):
    """
    题目选项 — 支持文字选项和图片选项。

    每道题有 2-6 个选项，is_correct 标记正确答案。
    单选题只允许一个 is_correct=True，多选题允许多个。
    """

    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='所属题目',
    )
    label = models.CharField(
        max_length=500,
        verbose_name='选项文字',
    )
    image = models.ImageField(
        upload_to='quiz/options/',
        blank=True,
        null=True,
        verbose_name='选项图片',
        help_text='图选题时使用',
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name='是否正确',
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='排序',
    )

    class Meta:
        db_table = 'quiz_option'
        ordering = ['order']
        verbose_name = '题目选项'
        verbose_name_plural = '题目选项列表'

    def __str__(self):
        mark = '✓' if self.is_correct else '✗'
        return f'{mark} {self.label[:40]}'


class UserQuizRecord(models.Model):
    """
    用户答题记录 — 支撑 UserProfile.vue 答题统计面板。

    通过聚合本表，计算 User.quiz_correct_count / quiz_total_count。
    同时在 MonumentArticle.vue 答对后解锁印章套色层（unlockedLayers++）。
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_records',
        verbose_name='用户',
    )
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name='user_records',
        verbose_name='题目',
    )
    is_correct = models.BooleanField(verbose_name='是否答对')
    selected_options = models.ManyToManyField(
        QuizOption,
        blank=True,
        related_name='user_selections',
        verbose_name='选择的选项',
    )
    points_earned = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='获得积分',
    )
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name='答题时间', db_index=True)

    class Meta:
        db_table = 'quiz_user_record'
        ordering = ['-answered_at']
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录列表'

    def __str__(self):
        result = '✓' if self.is_correct else '✗'
        return f'{self.user.username} {result} [{self.question.description[:30]}]'
