from django.contrib import admin

from .models import Project, ProjectPledge


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = ["title", "description"]
    list_display = ("__str__", "created")


@admin.register(ProjectPledge)
class ProjectPledgeAdmin(admin.ModelAdmin):
    ordering = ("-created",)
    list_display = ("__str__", "pledgee", "created")
    list_filter = ("project",)
