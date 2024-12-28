from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.support.models import News
from apps.support.tasks import send_news_to_subscribers


@receiver(post_save, sender=News)
def check_news_status(sender, instance, created, **kwargs):
    if created:
        send_news_to_subscribers.delay(instance.id)
