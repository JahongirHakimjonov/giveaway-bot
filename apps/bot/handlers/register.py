from django.utils.translation import gettext as _
from telebot import TeleBot
from telebot.types import CallbackQuery

from apps.bot.handlers.user import confirm_subscription
from apps.bot.logger import logger


def handle_callback_query(call: CallbackQuery, bot: TeleBot):
    if call.data == "confirm_subscription":
        confirm_subscription(call, bot)
        logger.info(f"User {call.from_user.id} selected a language.")
    else:
        bot.answer_callback_query(call.id, _("Unknown action."))
        logger.info(f"User {call.from_user.id} performed an unknown action.")
