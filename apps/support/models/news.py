from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5 MB
    if image.size > max_size:
        raise ValidationError(_("Rasm hajmi 5 MB dan katta bo'lmasligi kerak."))


class News(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    content = models.TextField(verbose_name=_("Maqola"))
    image = models.ImageField(
        upload_to="news/",
        verbose_name=_("Rasm"),
        validators=[validate_image_size],
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "news"
        verbose_name = _("Yangilik")
        verbose_name_plural = _("Yangiliklar")

    def __str__(self):
        return self.title
