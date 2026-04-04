from django.contrib import admin
from .models import SensitiveWord, AIConfig, AIInterceptionLog, NodeStatus


@admin.register(SensitiveWord)
class SensitiveWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'created_at')
    search_fields = ('word',)


@admin.register(AIConfig)
class AIConfigAdmin(admin.ModelAdmin):
    list_display = ('interception_strength', 'updated_at')


@admin.register(AIInterceptionLog)
class AIInterceptionLogAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'content_id', 'reason', 'intercepted_at')
    list_filter = ('content_type',)
    readonly_fields = ('intercepted_at',)


@admin.register(NodeStatus)
class NodeStatusAdmin(admin.ModelAdmin):
    list_display = ('node_index', 'load_percentage', 'recorded_at')
    list_filter = ('node_index',)
    readonly_fields = ('recorded_at',)
