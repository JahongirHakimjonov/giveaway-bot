import logging
import os
from time import sleep

from celery import shared_task
from django.utils.translation import activate
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

from apps.support.models import News, BotUsers, RoleChoices

bot = TeleBot(os.getenv("BOT_TOKEN"))

logger = logging.getLogger(__name__)


@shared_task()
def send_news_to_subscribers(news_id):
    try:
        sleep(5)
        news = News.objects.get(id=news_id)
        users = BotUsers.objects.all()
        admins = BotUsers.objects.filter(role=RoleChoices.ADMIN)
        message = f"{news.title}\n\n{news.content}"
        count = 0
        for user in users:
            try:
                if news.image:
                    # Agar rasm mavjud bo'lsa, rasmini yuboradi
                    bot.send_photo(
                        user.telegram_id,
                        photo=news.image.url,
                        caption=message,
                        parse_mode="Markdown",
                    )
                    logger.info(f"News sent to user {user.id}")
                else:
                    # Faqat matn yuborish
                    bot.send_message(
                        user.telegram_id, text=message, parse_mode="Markdown"
                    )
                    logger.info(f"News sent to user {user.id}")
                count += 1
            except ApiTelegramException as e:
                if e.error_code == 403:
                    print(f"User {user.id} has blocked the bot.")
                    logger.error(f"User {user.id} has blocked the bot.")
                    # Optionally, remove the user from the subscribers list
                    user.is_active = False
                    user.save()
                else:
                    logger.error(f"An error occurred: {e}")
        for admin in admins:
            try:
                bot.send_message(
                    admin.telegram_id,
                    text=f"Message sending {count} users",
                    parse_mode="Markdown",
                )
            except ApiTelegramException as e:
                if e.error_code == 403:
                    print(f"User {admin.id} has blocked the bot.")
                    # Optionally, remove the user from the subscribers list
                    admin.is_active = False
                    admin.save()
                else:
                    print(f"An error occurred: {e}")
    except News.DoesNotExist:
        print(f"News with id {news_id} does not exist.")
    except Exception as exc:
        print(f"An error occurred: {exc}")
