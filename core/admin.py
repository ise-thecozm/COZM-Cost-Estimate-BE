from django.contrib import admin
from .models import MobilityStateRecord, SavedEstimate


@admin.register(MobilityStateRecord)
class MobilityStateRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(SavedEstimate)
class SavedEstimateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'currency', 'total_cost', 'timestamp')
    list_filter = ('currency',)
    search_fields = ('name', 'user__username')
    readonly_fields = ('id', 'timestamp')
