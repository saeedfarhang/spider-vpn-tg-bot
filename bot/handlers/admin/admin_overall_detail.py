from telegram import InlineKeyboardButton, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from api.plans import get_plans
from bot.messages import ADMIN_OVERALL_DETAIL, SELECT_PLAN
from helpers import build_keyboard


async def admin_overall_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        [
            InlineKeyboardButton(
                "آخرین سفارش ها",
                callback_data={
                    "type": "admin",
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
            InlineKeyboardButton(
                "سفارش های در انتظار",
                callback_data={
                    "type": "admin",
                    "show_keyboard": True,
                    "data": {"action": "pending_approve_orders"},
                },
            ),
            InlineKeyboardButton(
                "ارسال پیام",
                callback_data={
                    "type": "admin",
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
        ],
        [
            InlineKeyboardButton(
                "ارسال پیام دسته جمعی",
                callback_data={
                    "type": "admin",
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
            InlineKeyboardButton(
                "تمدید اشتراک",
                callback_data={
                    "type": "admin",
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
        ],
        [
            InlineKeyboardButton(
                "لغو اشتراک",
                callback_data={
                    "type": "admin",
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
            InlineKeyboardButton(
                "درآمد",
                callback_data={
                    "type": "admin",
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
        ],
        [
            InlineKeyboardButton(
                "وضعیت سرور ها",
                callback_data={
                    "type": "admin",
                    "show_keyboard": True,
                    "data": {"action": ""},
                },
            ),
        ],
    ]
    await build_keyboard(update, ADMIN_OVERALL_DETAIL, reply_keyboard, False)
