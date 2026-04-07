from django.contrib import admin
from .models import Monument, UserMonumentProgress, ArticleSubmission, MonumentArticle, MonumentArticlePage


@admin.register(Monument)
class MonumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'dynasty', 'era', 'structure_type', 'location', 'is_published', 'created_at')
    search_fields = ('name', 'dynasty', 'location')
    list_filter = ('dynasty', 'is_published')
    list_editable = ('is_published',)


@admin.register(UserMonumentProgress)
class UserMonumentProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'monument', 'status', 'category_type', 'started_at', 'completed_at')
    list_filter = ('status', 'category_type')
    search_fields = ('user__username', 'monument__name')
    readonly_fields = ('started_at',)


@admin.register(ArticleSubmission)
class ArticleSubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'time')
    list_filter = ('status',)
    search_fields = ('title', 'author__username')
    readonly_fields = ('time',)
    actions = ['approve_submissions', 'reject_submissions']

    @admin.action(description='批量通过选中投稿')
    def approve_submissions(self, request, queryset):
        queryset.update(status=ArticleSubmission.STATUS_APPROVED)

    @admin.action(description='批量驳回选中投稿')
    def reject_submissions(self, request, queryset):
        queryset.update(status=ArticleSubmission.STATUS_REJECTED)


class MonumentArticlePageInline(admin.TabularInline):
    model = MonumentArticlePage
    extra = 1


@admin.register(MonumentArticle)
class MonumentArticleAdmin(admin.ModelAdmin):
    list_display = ('monument', 'title', 'page_count', 'created_at')
    search_fields = ('title', 'monument__name')
    inlines = [MonumentArticlePageInline]

    def page_count(self, obj):
        return obj.pages.count()
    page_count.short_description = '页数'


@admin.register(MonumentArticlePage)
class MonumentArticlePageAdmin(admin.ModelAdmin):
    list_display = ('article', 'page_number')
    list_filter = ('article',)
