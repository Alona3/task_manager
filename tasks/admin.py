from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Worker, Position, Team, Project, Tag, TaskType, Task


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ("username", "email", "position", "is_staff", "is_active")
    list_filter = ("position", "is_staff", "is_active")
    search_fields = ("username", "email")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("members",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "priority", "deadline", "is_completed", "project")
    list_filter = ("status", "priority", "deadline", "is_completed")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees", "tags")
