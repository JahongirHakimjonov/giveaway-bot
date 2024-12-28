import logging
import os

from celery import shared_task
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

from apps.support.models import BotUsers, Group, GroupType

bot = TeleBot(os.getenv("BOT_TOKEN"))

logger = logging.getLogger(__name__)


@shared_task()
def check_users_in_groups():
    users = BotUsers.objects.filter(is_active=True)
    groups = Group.objects.filter(is_active=True, group_type=GroupType.CHANNEL)
    for user in users:
        for group in groups:
            try:
                member = bot.get_chat_member(group.group_id, user.telegram_id)
                if member.status == "left" or member.status == "kicked":
                    logger.info(
                        f"User {user.telegram_id} has left or was kicked from group {group.group_id}."
                    )
                    user.code = None
                    user.save()
                    bot.send_message(
                        user.telegram_id,
                        "❗️ Diqqat! Siz homiy kanallardan chiqib ketgansiz.\n\n🔄 Konkursda ishtirokni davom ettirish uchun:\n1️⃣ /start tugmasini bosing.\n2️⃣ Homiy kanallarga qayta obuna bo‘ling.\n\n🎯 Yutish imkoniyatini qo‘ldan boy bermang!",
                    )
                else:
                    logger.info(
                        f"User {user.telegram_id} is still in group {group.group_id}."
                    )
            except ApiTelegramException as e:
                logger.error(
                    f"An error occurred while checking user {user.telegram_id} in group {group.group_id}: {e}"
                )
