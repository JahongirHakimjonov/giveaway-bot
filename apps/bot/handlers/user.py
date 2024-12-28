import base64
import re

import telebot
from django.utils import timezone
from django.utils.translation import gettext as _
from telebot import TeleBot, types
from telebot.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.support.models import Group, BotUsers, GroupType


def any_user(message: Message, bot: TeleBot):
    try:
        update_or_create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            is_active=True,
        )
        logger.info(f"User {message.from_user.id} started the bot.")

        # Ask for phone number
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button = KeyboardButton(_("📱Raqamni ulashish"), request_contact=True)
        markup.add(button)
        bot.send_message(
            message.chat.id,
            _(
                "Iltimos, menga telefon raqamingizni yuboring.\n\n"
                "Ekran pastidagi *Raqamni ulashish* tugmasini bosing 👇"
            ),
            reply_markup=markup,
            parse_mode="Markdown",
        )
        bot.register_next_step_handler(message, handle_phone, bot)
    except Exception as e:
        bot.send_message(message.chat.id, _("Xatolik yuz berdi."))
        logger.error(f"Error in any_user: {e}")


def handle_phone(message: Message, bot: TeleBot):
    phone = None
    regex_pattern = r"^\+?998[\d\s\-\(\)]{9}$"

    if message.contact:
        phone = message.contact.phone_number
    elif message.text and re.match(regex_pattern, message.text):
        phone = re.sub(r"[^\d]", "", message.text)
    else:
        bot.send_message(
            message.chat.id,
            _("Yaroqsiz telefon raqam formati. Iltimos, qayta urinib ko'ring."),
        )
        logger.info(f"User {message.from_user.id} entered an invalid phone number.")
        bot.register_next_step_handler(message, handle_phone, bot)
        return

    user = BotUsers.objects.get(telegram_id=message.from_user.id)
    user.phone = phone
    user.save()
    logger.info(f"User {message.from_user.id} entered phone number: {phone}")

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    regions = Group.objects.filter(is_active=True)
    buttons = [
        types.InlineKeyboardButton(text=region.name, url=region.url)
        for region in regions
    ]
    confirm = types.InlineKeyboardButton(
        text=_("✅ Tasdiqlash"), callback_data="confirm_subscription"
    )
    keyboard.add(*buttons)
    keyboard.add(confirm)
    reply_markup = ReplyKeyboardRemove()
    bot.send_message(
        message.chat.id, _("Telfon raqam saqlandi!"), reply_markup=reply_markup
    )
    bot.send_message(
        message.chat.id,
        _(
            "Konkursga qatnashish uchun bizning barcha homiylarimizga obuna bo'ling va *✅ Tasdiqlash* ni bosing."
        ),
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    logger.info(f"User {message.from_user.id} asked to confirm subscription.")


def confirm_subscription(call: CallbackQuery, bot: TeleBot):
    user_id = call.from_user.id

    groups = Group.objects.filter(is_active=True, group_type=GroupType.CHANNEL)
    for group in groups:
        try:
            username = group.url.replace("https://t.me/", "@")
            chat_member = bot.get_chat_member(username, user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                bot.answer_callback_query(
                    call.id,
                    _(
                        f"❗️Siz homiy kanallarga hali obuna bo'lmadingiz, kanallarga obuna bo'ling va Tasdiqlash tugmasini bosing.\n\n🎯Yutish imkoniyatini boy bermang!"
                        f"\n\n👉 {group.name} Obuna bo'ling"
                    ),
                    show_alert=True,
                )
                logger.info(f"User {user_id} is not subscribed to {group.name}.")
                return
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 400:
                if "query is too old" in e.result_json.get("description", ""):
                    bot.answer_callback_query(
                        call.id,
                        _(
                            "Xatolik yuz berdi: so'rov eskirgan. Iltimos, qayta urinib ko'ring."
                        ),
                        show_alert=True,
                    )
                    logger.info(
                        f"User {user_id} tried to confirm subscription with an old query."
                    )
                else:
                    bot.send_message(
                        call.message.chat.id,
                        _(
                            "Xatolik yuz berdi: chat topilmadi. Bot kanallarda admin qilinmagan Iltimos, qayta urinib ko'ring."
                        ),
                    )
                    logger.info(
                        f"User {user_id} tried to confirm subscription with an unknown error."
                    )
            else:
                bot.send_message(
                    call.message.chat.id,
                    _("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."),
                )
            logger.error(f"Error in confirm_subscription: {e}")
            return

    user_id_bytes = str(user_id).encode("utf-8")
    base64_user_id = base64.b64encode(user_id_bytes).decode("utf-8")
    user = BotUsers.objects.filter(telegram_id=user_id).first()
    user.code = base64_user_id
    user.code_get_time = timezone.now()
    user.save()
    bot.send_message(
        call.message.chat.id,
        _(
            f"🎉 Tabriklaymiz! Siz muvaffaqiyatli obuna bo'ldingiz!\n\n👉 Sizning maxsus kodingiz:  `{base64_user_id}`"
        ),
        parse_mode="Markdown",
    )
    logger.info(f"User {user_id} successfully subscribed to all groups.")
