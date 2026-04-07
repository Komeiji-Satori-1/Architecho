from django.contrib import admin
from .models import QuizQuestion, QuizOption, UserQuizRecord


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 2


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('description_short', 'question_type', 'monument', 'points', 'created_at')
    search_fields = ('description',)
    list_filter = ('question_type', 'monument')
    inlines = [QuizOptionInline]

    def description_short(self, obj):
        return obj.description[:60]
    description_short.short_description = '题目描述'


@admin.register(UserQuizRecord)
class UserQuizRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_correct', 'points_earned', 'answered_at')
    list_filter = ('is_correct',)
    search_fields = ('user__username',)
