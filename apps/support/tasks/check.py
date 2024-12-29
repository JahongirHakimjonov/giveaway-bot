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
        not_in_groups = []
        for group in groups:
            try:
                member = bot.get_chat_member(group.group_id, user.telegram_id)
                if member.status == "left" or member.status == "kicked":
                    # not_in_groups.append(group.group_id)
                    url = group.url
                    username = url.replace("https://t.me/", "@")
                    not_in_groups.append(username)
            except ApiTelegramException as e:
                logger.error(
                    f"An error occurred while checking user {user.telegram_id} in group {group.group_id}: {e}"
                )

        if not_in_groups:
            logger.info(
                f"User {user.telegram_id} has left or was kicked from groups: {', '.join(not_in_groups)}."
            )
            user.code = None
            user.save()
            bot.send_message(
                user.telegram_id,
                f"❗️ Diqqat! Siz homiy kanallardan chiqib ketgansiz:\n{' , '.join(not_in_groups)} .\n\n"
                "🔄 Konkursda ishtirokni davom ettirish uchun:\n"
                "1️⃣ /start tugmasini bosing.\n"
                "2️⃣ Homiy kanallarga qayta obuna bo‘ling.\n\n"
                "🎯 Yutish imkoniyatini qo‘ldan boy bermang!"
            )
