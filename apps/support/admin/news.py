from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.support.models import News


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)
