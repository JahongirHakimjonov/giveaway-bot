from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.support.models import Info, InfoLinks
from modeltranslation.admin import TabbedTranslationAdmin


class InfoLinksInline(TabularInline):
    model = InfoLinks
    extra = 1


@admin.register(Info)
class InfoAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "info",
        "created_at",
    )
    search_fields = (
        "info",
        "full_name",
    )
    list_filter = ("created_at", "updated_at")
    list_filter_submit = True
    list_display_links = ("id", "full_name", "info")
    inlines = (InfoLinksInline,)


@admin.register(InfoLinks)
class InfoLinksAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "link",
        "created_at",
    )
    search_fields = (
        "name",
        "link",
    )
    list_filter = ("created_at", "updated_at")
    list_filter_submit = True
    list_display_links = ("id", "name", "link")
