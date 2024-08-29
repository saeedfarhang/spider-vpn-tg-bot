import logging
from bot.messages import COMPLETE_ORDER_HEAD_TEXT, DUPLICATE_TEST_ACCOUNT
from helpers.json_to_str import outline_config_json_to_str
from telegram.ext import Application
from telegram.constants import ParseMode

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
        vpn_config = order["expand"]["vpn_config"]
        connection_data = vpn_config["connection_data"]
        connection_data_str = outline_config_json_to_str(
            COMPLETE_ORDER_HEAD_TEXT, connection_data
        )
        await application.bot.send_message(
            chat_id=user_id, text=connection_data_str, parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error("Failed to send message: %s", e)
