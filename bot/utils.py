import logging

from telegram import Update
from telegram.ext import ContextTypes

from api.order_approval import create_order_approval
from api.orders import get_order_by_id
from bot.messages import WAIT_FOR_APPROVE

logger = logging.getLogger(__name__)


async def approve_pending_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo_file = await update.message.photo[-1].get_file()
    photo_tg_id = photo_file.file_id
    photo_path = f"tmp/order_approval/{photo_file.file_unique_id}.jpg"
    await photo_file.download_to_drive(photo_path)

    user_id = update.effective_chat.id
    if order_id := context.user_data.get("order_id"):
        get_order_by_id(order_id, user_id)
        await create_order_approval(photo_path, photo_tg_id, order_id, user_id)

    await update.message.reply_text(text=WAIT_FOR_APPROVE)
