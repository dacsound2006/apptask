from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("code", "project", "phase", "name", "owner", "due", "status", "progress", "is_late")
    list_filter = ("project", "phase", "status", "owner")
    search_fields = ("code", "name", "owner")
    list_editable = ("status", "progress")
    ordering = ("due", "code")
