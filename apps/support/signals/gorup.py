import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from telebot import TeleBot

from apps.support.models import Group

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)


def get_channel_id(channel_username):
    try:
        chat = bot.get_chat(channel_username)
        return chat.id
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return None


@receiver(post_save, sender=Group)
def check_group_status(sender, instance, created, **kwargs):
    if created:
        url = instance.url
        print(url)
        url = url.replace("https://t.me/", "@")
        print(url)
        channel_id = get_channel_id(url)
        instance.group_id = channel_id
        instance.save()
