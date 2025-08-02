from django.contrib import admin
from .models import Issue, IssuePhoto, StatusHistory, Flag

class IssuePhotoInline(admin.TabularInline):
    model = IssuePhoto
    extra = 0

class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0

class FlagInline(admin.TabularInline):
    model = Flag
    extra = 0

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_at', 'user')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')
    inlines = [IssuePhotoInline, StatusHistoryInline, FlagInline]

admin.site.register(IssuePhoto)
admin.site.register(StatusHistory)
admin.site.register(Flag)
