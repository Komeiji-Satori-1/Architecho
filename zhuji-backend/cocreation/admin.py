from django.contrib import admin
from .models import CoCreationItem, CoCreationImage


class CoCreationImageInline(admin.TabularInline):
    model = CoCreationImage
    extra = 0


@admin.register(CoCreationItem)
class CoCreationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'material', 'status', 'progress_percent', 'featured', 'likes', 'created_at')
    list_filter = ('status', 'material', 'featured')
    search_fields = ('title', 'author__username')
    list_editable = ('featured', 'status', 'progress_percent')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CoCreationImageInline]
