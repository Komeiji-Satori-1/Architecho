from django.contrib import admin
from .models import Stamp, StampColorLayer, UserStamp


class StampColorLayerInline(admin.TabularInline):
    model = StampColorLayer
    extra = 0


@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    list_display = ('name', 'monument', 'total_layers', 'collected_count')
    search_fields = ('name', 'monument__name')
    inlines = [StampColorLayerInline]

    def collected_count(self, obj):
        return obj.collectors.filter(unlocked_layers__gt=0).count()
    collected_count.short_description = '已收集用户数'


@admin.register(UserStamp)
class UserStampAdmin(admin.ModelAdmin):
    list_display = ('user', 'stamp', 'unlocked_layers', 'collected_at')
    list_filter = ('stamp',)
    search_fields = ('user__username', 'stamp__name')
    readonly_fields = ('collected_at',)
