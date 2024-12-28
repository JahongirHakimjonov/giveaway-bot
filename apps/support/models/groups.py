from django.db.models import (
    BigIntegerField,
    BooleanField,
    CharField,
)
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Group(AbstractBaseModel):
    name = CharField(max_length=255, verbose_name=_("Kanal nomi"))
    url = CharField(max_length=255, verbose_name=_("Kanal URL"), null=True, blank=True)
    group_id = BigIntegerField(verbose_name=_("Kanal ID"), null=True, blank=True)
    is_active = BooleanField(default=True, verbose_name=_("Faolmi"))

    def __str__(self) -> str:
        return f"{self.name} - {self.group_id}"

    class Meta:
        db_table = "groups"
        verbose_name = _("Kanal")
        verbose_name_plural = _("Kanallar")
        ordering = ["name"]
