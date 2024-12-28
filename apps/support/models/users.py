from django.db.models import (
    BigIntegerField,
    BooleanField,
    CharField,
    TextChoices,
)
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class RoleChoices(TextChoices):
    ADMIN = "admin", _("Admin")
    MODERATOR = "moderator", _("Moderator")
    USER = "user", _("Foydalanuvchi")


class LanguageChoices(TextChoices):
    UZ = "uz", _("O'zbek tili")
    RU = "ru", _("Rus tili")
    EN = "en", _("Ingliz tili")


class BotUsers(AbstractBaseModel):
    telegram_id = BigIntegerField(unique=True, verbose_name=_("Telegram ID"))
    username = CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Foydalanuvchi nomi"),
    )
    first_name = CharField(max_length=255, null=True, blank=True, verbose_name=_("Ism"))
    last_name = CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Familiya")
    )
    full_name = CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Ism va Familiya")
    )
    phone = BigIntegerField(
        null=True, blank=True, unique=True, verbose_name=_("Telefon raqam")
    )
    language_code = CharField(
        max_length=10,
        choices=LanguageChoices.choices,
        default=LanguageChoices.UZ,
        verbose_name=_("Til"),
    )
    is_active = BooleanField(default=True, verbose_name=_("Faolmi"))
    role = CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        verbose_name=_("Rol"),
    )
    code = CharField(max_length=100, null=True, blank=True, verbose_name=_("Kod"))

    class Meta:
        db_table = "bot_users"
        verbose_name = _("Bot Foydalanuvchisi")
        verbose_name_plural = _("Bot Foydalanuvchilari")

    def __str__(self):
        return str(self.first_name if self.first_name else _("Bot Foydalnuvchisi"))
