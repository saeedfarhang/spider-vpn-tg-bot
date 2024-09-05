import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from api.order_approval import create_order_approval, get_order_approvals
from api.orders import get_order_by_id
from bot.messages import (
    COMPLETE_ORDER_HEAD_TEXT,
    CONNECTION_TUTORIAL_LINKS,
    DUPLICATE_TEST_ACCOUNT,
    EXPIRY_NOTIFICATION,
    NEW_ORDER_APPROVAL,
    ORDER_CREATED_WITHOUT_DATA,
    WAIT_FOR_APPROVE,
)
from helpers.enums.inline_button_click_types import InlineButtonClickTypes
from helpers.json_to_str import outline_config_json_to_str
from telegram.ext import Application
from telegram.constants import ParseMode

from telegram.ext import (
    ContextTypes,
)

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
