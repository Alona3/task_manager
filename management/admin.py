from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from management.models import (
    Worker, Position, ProjectType, Project, Team
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "team_lead", "number_of_members",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = (
        "username",
        "get_full_name",
        "email",
        "position",
    )
    search_fields = ("username", "first_name", "last_name", "position__name")
    ordering = ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional information",
            {
                "fields": ("position", "team"),
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional information",
            {
                "fields": (
                    "first_name", "last_name", "email", "position", "team"
                ),
            },
        ),
    )

    def get_full_name(self, obj) -> str:
        return f"{obj.first_name} {obj.last_name}"

    get_full_name.short_description = "full_name"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "deadline", "priority", "is_completed")
    search_fields = ("name", "project_type__name")
