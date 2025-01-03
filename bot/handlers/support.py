from telegram import Update
from telegram.ext import ContextTypes

from bot.state import SELECT_MAIN_ITEM


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "support",
    )
    return SELECT_MAIN_ITEM
