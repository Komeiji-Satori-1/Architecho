from django.contrib import admin
from .models import ForumCategory, ForumPost, PostImage, Comment


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'hot', 'sort_order', 'post_count')
    list_editable = ('hot', 'sort_order')
    search_fields = ('name',)

    def post_count(self, obj):
        return obj.post_count
    post_count.short_description = '帖子数'


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_top', 'is_essence', 'views', 'likes', 'created_at')
    list_filter = ('is_top', 'is_essence', 'category')
    search_fields = ('title', 'author__username')
    readonly_fields = ('views', 'likes', 'created_at', 'updated_at')
    inlines = [PostImageInline]
    actions = ['mark_essence', 'mark_top']

    @admin.action(description='设为精华帖')
    def mark_essence(self, request, queryset):
        queryset.update(is_essence=True)

    @admin.action(description='设为置顶帖')
    def mark_top(self, request, queryset):
        queryset.update(is_top=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text_short', 'parent', 'likes', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'text')
    readonly_fields = ('created_at',)

    def text_short(self, obj):
        return obj.text[:60]
    text_short.short_description = '内容'
