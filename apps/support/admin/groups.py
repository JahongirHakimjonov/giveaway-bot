from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.support.models import Group


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "group_id",
        "url",
        "is_active",
        "created_at",
    )
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    list_editable = ("is_active",)
    list_filter_submit = True
    list_display_links = ("id", "name", "group_id")
