from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from bot.messages import ADMIN_OVERALL_DETAIL
from helpers import build_keyboard
from helpers.enums.inline_button_click_types import InlineButtonClickTypes


async def admin_overall_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        [
            InlineKeyboardButton(
                "آخرین سفارش ها",
                callback_data={
                    "type": InlineButtonClickTypes.ADMIN,
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
            InlineKeyboardButton(
                "سفارش های در انتظار",
                callback_data={
                    "type": InlineButtonClickTypes.ADMIN,
                    "show_keyboard": True,
                    "data": {"action": "pending_approve_orders"},
                },
            ),
            InlineKeyboardButton(
                "ارسال پیام",
                callback_data={
                    "type": InlineButtonClickTypes.ADMIN,
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
        ],
        [
            InlineKeyboardButton(
                "ارسال پیام دسته جمعی",
                callback_data={
                    "type": InlineButtonClickTypes.ADMIN,
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
            InlineKeyboardButton(
                "تمدید اشتراک",
                callback_data={
                    "type": InlineButtonClickTypes.ADMIN,
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
        ],
        [
            InlineKeyboardButton(
                "لغو اشتراک",
                callback_data={
                    "type": InlineButtonClickTypes.ADMIN,
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
            InlineKeyboardButton(
                "درآمد",
                callback_data={
                    "type": InlineButtonClickTypes.ADMIN,
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
        ],
        [
            InlineKeyboardButton(
                "وضعیت سرور ها",
                callback_data={
                    "type": InlineButtonClickTypes.ADMIN,
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
        ],
    ]
    await build_keyboard(update, ADMIN_OVERALL_DETAIL, reply_keyboard, False)
