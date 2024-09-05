from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from bot.messages import SELECT_HOW_TO_CONNECT_SELECT_PLATFORM
from helpers import build_keyboard
from helpers.enums.inline_button_click_types import InlineButtonClickTypes


async def how_to_connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    reply_keyboard = [
        [
            InlineKeyboardButton(
                "راهنمای ویندوز",
                callback_data={
                    "type": InlineButtonClickTypes.HOW_TO_CONNECT,
                    "platform": "WINDOWS",
                },
            ),
            InlineKeyboardButton(
                "راهنمای اندروید",
                callback_data={
                    "type": InlineButtonClickTypes.HOW_TO_CONNECT,
                    "platform": "ANDROID",
                },
            ),
        ],
        [
            InlineKeyboardButton(
                "دیگر پلتفرم ها",
                callback_data={
                    "type": InlineButtonClickTypes.HOW_TO_CONNECT,
                    "platform": "OTHER",
                },
            ),
            InlineKeyboardButton(
                "راهنمای iOS",
                callback_data={
                    "type": InlineButtonClickTypes.HOW_TO_CONNECT,
                    "platform": "IOS",
                },
            ),
        ],
    ]
    if query:
        await build_keyboard(
            query, SELECT_HOW_TO_CONNECT_SELECT_PLATFORM, reply_keyboard, False
        )
    else:
        await build_keyboard(
            update, SELECT_HOW_TO_CONNECT_SELECT_PLATFORM, reply_keyboard, False
        )
