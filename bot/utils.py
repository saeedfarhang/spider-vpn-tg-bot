import logging
from telegram import Update
from api.order_approval import create_order_approval
from api.orders import get_order_by_id
from bot.messages import (
    COMPLETE_ORDER_HEAD_TEXT,
    CONNECTION_TUTORIAL_LINKS,
    DUPLICATE_TEST_ACCOUNT,
    EXPIRY_NOTIFICATION,
    ORDER_CREATED_WITHOUT_DATA,
    WAIT_FOR_APPROVE,
)
from helpers.json_to_str import outline_config_json_to_str
from telegram.ext import Application
from telegram.constants import ParseMode

from telegram.ext import (
    ContextTypes,
)

logger = logging.getLogger(__name__)


async def send_duplicate_test_account_message_to_user(
    application: Application, user_id
):
    try:
        await application.bot.send_message(chat_id=user_id, text=DUPLICATE_TEST_ACCOUNT)
    except Exception as e:
        logger.error("Failed to send message: %s", e)


async def send_vpn_config_to_user(application: Application, user_id, order):
    try:
        connection_data_str = outline_config_json_to_str(
            COMPLETE_ORDER_HEAD_TEXT, order
        )
        await application.bot.send_message(
            chat_id=user_id,
            text=connection_data_str + f"\n\n{CONNECTION_TUTORIAL_LINKS}",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        logger.error("Failed to send message: %s", e)
        await application.bot.send_message(
            chat_id=user_id,
            text=ORDER_CREATED_WITHOUT_DATA,
            parse_mode=ParseMode.MARKDOWN,
        )


async def send_request_error_notification_to_user(
    application: Application, user_id: int, status: int
):
    await application.bot.send_message(
        chat_id=user_id, text="connection_data_str", parse_mode=ParseMode.MARKDOWN
    )


async def send_vpn_config_expiry_notification_to_user(
    application: Application,
    user_id,
    order_id: str,
    hours_to_expire: int,
    remain_in_mb: int,
):
    try:

        await application.bot.send_message(
            chat_id=user_id,
            text=EXPIRY_NOTIFICATION.format(order_id, hours_to_expire, remain_in_mb),
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        logger.error("Failed to send message: %s", e)


async def send_vpn_config_deprecated_notification_to_user(
    application: Application, user_id, order_id: str
):
    try:

        await application.bot.send_message(
            chat_id=user_id, text="test", parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error("Failed to send message: %s", e)
        await application.bot.send_message(
            chat_id=user_id,
            text="ORDER_CREATED_WITHOUT_DATA",
            parse_mode=ParseMode.MARKDOWN,
        )


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
