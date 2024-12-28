from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.support.models import BotUsers, LanguageChoices, RoleChoices


@admin.register(BotUsers)
class BotUsersAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = (
        "id",
        "telegram_id_with_color",
        "username",
        "language_code_with_color",
        "role_with_color",
        "code",
        "created_at",
    )
    search_fields = (
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "phone",
        "full_name",
    )
    list_filter = ("created_at", "updated_at", "is_active", "role", "language_code")
    list_filter_submit = True
    list_display_links = ("id", "telegram_id_with_color", "username")

    @display(
        description=_("Til"),
        label={
            LanguageChoices.UZ: "info",
            LanguageChoices.RU: "info",
            LanguageChoices.EN: "info",
        },
    )
    def language_code_with_color(self, obj):
        return obj.language_code, obj.get_language_code_display()

    @display(
        description=_("Rol"),
        label={
            RoleChoices.USER: "warning",
            RoleChoices.MODERATOR: "info",
            RoleChoices.ADMIN: "success",
        },
    )
    def role_with_color(self, obj):
        return obj.role, obj.get_role_display()

    @display(description=_("Telegram ID"), label=True)
    def telegram_id_with_color(self, obj):
        return obj.telegram_id
