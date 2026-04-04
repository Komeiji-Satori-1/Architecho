from django.conf import settings
from django.db import models


class QuizQuestion(models.Model):
    """
    古建知识题库条目 — 对应 StampDiscovery.vue 答题区。

    前端题型为图选题（2–4 张图片选一），字段映射：
      description    → "1. 下图中展示的斗拱结构中，哪一部分被称为'下昂'？"
      correct_answer → 正确答案文字描述
      distractor_a/b → 干扰项 A/B（前端 AdminDashboard 题库录入表单对应字段）
      image          → 题目参考图（StampDiscovery 图选题 quizOptions[].image）
      monument       → 可选关联古建，用于集章学习路径
    """

    description = models.TextField(verbose_name='题目描述')
    correct_answer = models.CharField(max_length=200, verbose_name='正确答案')
    distractor_a = models.CharField(max_length=200, verbose_name='干扰项 A')
    distractor_b = models.CharField(max_length=200, verbose_name='干扰项 B')
    image = models.ImageField(
        upload_to='quiz/',
        blank=True,
        null=True,
        verbose_name='参考图',
        help_text='图选题主图，对应 StampDiscovery.quizOptions[].image',
    )
    monument = models.ForeignKey(
        'monuments.Monument',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quiz_questions',
        verbose_name='关联古建',
        help_text='题目归属的古建学习路径',
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


class UserQuizRecord(models.Model):
    """
    用户答题记录 — 支撑 UserProfile.vue 答题统计面板。

    对应前端数据：
      "在 240 个古建知识点中 / 答题正确率 89% / 领先 92% 的营造师"
    通过聚合本表，计算 User.quiz_correct_count / quiz_total_count。
    同时在 StampDiscovery.vue 答对后解锁印章套色层（unlockedLayers++）。
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
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name='答题时间', db_index=True)

    class Meta:
        db_table = 'quiz_user_record'
        ordering = ['-answered_at']
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录列表'

    def __str__(self):
        result = '✓' if self.is_correct else '✗'
        return f'{self.user.username} {result} [{self.question.description[:30]}]'
