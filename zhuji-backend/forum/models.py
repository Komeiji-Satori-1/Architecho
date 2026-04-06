from django.conf import settings
from django.db import models


class ForumCategory(models.Model):
    """
    论坛板块 — 对应 ForumList.vue categories 侧边栏。

    字段映射：
      name  → cat.name  ('营造法式'|'古建摄影'|'模型制作'|'木作工艺'|'彩画装饰')
      hot   → cat.hot   (Hot 标签)
      count → post_count 属性（帖子总数，"2.4k"）
      sort_order → 前端展示顺序
    """

    name = models.CharField(max_length=100, unique=True, verbose_name='板块名称')
    hot = models.BooleanField(default=False, verbose_name='热门标记', db_index=True)
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name='排序权重')

    class Meta:
        db_table = 'forum_category'
        ordering = ['-hot', 'sort_order']
        verbose_name = '论坛板块'
        verbose_name_plural = '论坛板块列表'

    def __str__(self):
        return self.name

    @property
    def post_count(self) -> int:
        return self.posts.count()


class ForumPost(models.Model):
    """
    论坛帖子 — 同时对应三个前端场景：

    1. ForumList.vue posts 列表卡片:
       id, title, excerpt, author, authorAvatar→author.avatar,
       category, time, views, likes, comments(count),
       isTop, isEssence, images?[]

    2. PostDetail.vue 帖子详情:
       content(段落数组), lastEdit, likes(可点赞互动)

    3. PostCard.vue 组件 Props:
       id, title, cover(封面图), category, author, views, comments
    """

    title = models.CharField(max_length=300, verbose_name='标题')
    excerpt = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='摘要',
        help_text='帖子列表卡片展示的简短摘要，对应 post.excerpt',
    )
    content = models.TextField(
        verbose_name='正文内容',
        help_text='完整富文本内容。前端以段落数组形式展示：post.content[]',
    )
    cover = models.ImageField(
        upload_to='forum/covers/',
        blank=True,
        null=True,
        verbose_name='封面图',
        help_text='PostCard.vue post.cover',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_posts',
        verbose_name='作者',
    )
    category = models.ForeignKey(
        ForumCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='板块',
    )

    # ---- ForumList.vue: isTop, isEssence ----
    # PostDetail.vue: 管理员可切换置顶/加精
    is_top = models.BooleanField(default=False, verbose_name='是否置顶', db_index=True)
    is_essence = models.BooleanField(default=False, verbose_name='是否精华')

    # ---- 统计字段 ----
    # views "1.2w"，likes "856"
    views = models.PositiveIntegerField(default=0, verbose_name='浏览数')
    likes = models.PositiveIntegerField(default=0, verbose_name='点赞数')

    # ---- 时间字段 ----
    # time "3小时前" / "2024-03-20"，lastEdit "2024-03-21 14:30"
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'forum_post'
        ordering = ['-is_top', '-created_at']
        verbose_name = '论坛帖子'
        verbose_name_plural = '论坛帖子列表'

    def __str__(self):
        return self.title

    @property
    def comment_count(self) -> int:
        """前端 post.comments 数量，仅统计一级评论。"""
        return self.comments.filter(parent__isnull=True).count()

    @property
    def last_edit(self) -> str:
        """前端 post.lastEdit 格式：'2024-03-21 14:30'。"""
        return self.updated_at.strftime('%Y-%m-%d %H:%M')


class PostImage(models.Model):
    """
    帖子图片 — 对应 ForumList.vue post.images[] 和 PostDetail.vue post.images[]。

    前端展示：
      ForumList  → grid grid-cols-3 最多展示3张（slice(0,3)）
      PostDetail → 全量展示，每张独立大图
    """

    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='关联帖子',
    )
    image = models.ImageField(upload_to='forum/images/', verbose_name='图片')
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'forum_post_image'
        ordering = ['sort_order']
        verbose_name = '帖子图片'
        verbose_name_plural = '帖子图片列表'


class CommentImage(models.Model):
    """一级评论配图，最多5张。"""

    comment = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='关联评论',
    )
    image = models.ImageField(upload_to='forum/comment_images/', verbose_name='图片')
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'forum_comment_image'
        ordering = ['sort_order']
        verbose_name = '评论图片'
        verbose_name_plural = '评论图片列表'


class Comment(models.Model):
    """
    评论与回复 — 对应 PostDetail.vue comments（含二级嵌套 replies）。

    字段映射：
      author      → comment.author（用户名）
      author.avatar → comment.avatar
      text        → comment.text
      likes       → comment.likes (赞同 24)
      created_at  → comment.time ("2小时前"，serializer 输出相对时间)
      parent      → 自关联：null=一级评论，非null=回复（replies[]）

    二级嵌套逻辑（PostDetail.vue）：
      reply.author → reply.author
      reply.text   → reply.text
      "回复 @comment.author" → 前端固定文案，后端只需提供 parent_id
    """

    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='关联帖子',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='评论者',
    )
    text = models.TextField(verbose_name='内容')
    likes = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    # 二级嵌套：parent=None 表示一级评论；parent=Comment 表示对某条一级评论的回复
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='父评论',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间', db_index=True)

    class Meta:
        db_table = 'forum_comment'
        ordering = ['created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论列表'

    def __str__(self):
        return f'{self.author.username}: {self.text[:50]}'
