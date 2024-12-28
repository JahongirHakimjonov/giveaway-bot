from django.db.models import (
    BigIntegerField,
    BooleanField,
    CharField,
    DateField,
    TextField,
    URLField,
    ForeignKey,
    CASCADE,
    ImageField,
)
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Info(AbstractBaseModel):
    full_name = CharField(max_length=255, verbose_name=_("Ism va Familiya"))
    birth_date = DateField(verbose_name=_("Tug'ilgan kun"))
    age = BigIntegerField(verbose_name=_("Yosh"))
    info = TextField(verbose_name=_("Ma'lumot"))
    photo = ImageField(upload_to="info", verbose_name=_("Rasm"))
    is_active = BooleanField(default=True, verbose_name=_("Faolmi"))

    def __str__(self) -> str:
        return f"{self.full_name} - {self.age} yosh"

    def calculate_age(self):
        from datetime import date

        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "info"
        verbose_name = _("Info")
        verbose_name_plural = _("Infos")


class InfoLinks(AbstractBaseModel):
    info = ForeignKey(Info, on_delete=CASCADE, verbose_name=_("Ma'lumot"))
    name = CharField(max_length=255, verbose_name=_("Ma'lumot"))
    link = URLField(verbose_name=_("Link"))
    is_active = BooleanField(default=True, verbose_name=_("Faolmi"))

    def __str__(self) -> str:
        return f"{self.info} - {self.link}"

    class Meta:
        db_table = "info_links"
        verbose_name = _("Info Links")
        verbose_name_plural = _("Info Links")
