from django.contrib import admin
from .models import QuizQuestion


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('description_short', 'correct_answer', 'monument', 'created_at')
    search_fields = ('description', 'correct_answer')
    list_filter = ('monument',)

    def description_short(self, obj):
        return obj.description[:60]
    description_short.short_description = '题目描述'
