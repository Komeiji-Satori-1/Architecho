from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SensitiveWord(models.Model):
    """
    敏感词库条目，对应前端 keywords 数组。
    前端展示为 chip 标签，支持删除和新增。
    """
    word = models.CharField(max_length=100, unique=True, verbose_name='敏感词')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'system_sensitive_word'
        ordering = ['word']
        verbose_name = '敏感词'
        verbose_name_plural = '敏感词库'

    def __str__(self):
        return self.word


class AIConfig(models.Model):
    """
    AI 监管配置（单例模式，只存一条记录）。
    interception_strength 对应前端"自动拦截强度"滑块 (1–100)。
    """
    interception_strength = models.IntegerField(
        default=75,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='自动拦截强度',
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'system_ai_config'
        verbose_name = 'AI 监管配置'
        verbose_name_plural = 'AI 监管配置'

    def __str__(self):
        return f'AI 配置（强度 {self.interception_strength}）'


class AIInterceptionLog(models.Model):
    """
    AI 拦截日志，用于统计大盘"AI 拦截率（次/日）"指标。
    """
    content_type = models.CharField(
        max_length=50,
        verbose_name='内容类型',
        help_text='如 submission、comment 等',
    )
    content_id = models.PositiveIntegerField(verbose_name='内容 ID')
    reason = models.TextField(verbose_name='拦截原因')
    intercepted_at = models.DateTimeField(auto_now_add=True, verbose_name='拦截时间', db_index=True)

    class Meta:
        db_table = 'system_ai_interception_log'
        ordering = ['-intercepted_at']
        verbose_name = 'AI 拦截日志'
        verbose_name_plural = 'AI 拦截日志'

    def __str__(self):
        return f'{self.content_type}#{self.content_id} @ {self.intercepted_at:%Y-%m-%d %H:%M}'


class NodeStatus(models.Model):
    """
    系统节点负载模拟数据，对应前端"系统健康度"面板（节点 N 负载）。
    每次采集时写入一条记录，前端取最新 3 条节点数据展示。
    """
    node_index = models.PositiveSmallIntegerField(verbose_name='节点编号', db_index=True)
    load_percentage = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        verbose_name='负载百分比',
    )
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name='采集时间', db_index=True)

    class Meta:
        db_table = 'system_node_status'
        ordering = ['-recorded_at']
        verbose_name = '节点状态'
        verbose_name_plural = '节点状态记录'

    def __str__(self):
        return f'节点 {self.node_index}：{self.load_percentage:.1f}%'
