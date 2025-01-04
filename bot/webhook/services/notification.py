from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application

from api.order_approval import get_order_approvals
from bot.messages import (COMPLETE_ORDER_HEAD_TEXT, CONNECTION_TUTORIAL_LINKS,
                          DUPLICATE_TEST_ACCOUNT, ERROR_NOTIFICATIONS,
                          EXPIRY_NOTIFICATION, NEW_ORDER_APPROVAL,
                          ORDER_CREATED_WITHOUT_DATA, SERVERS_HEALTH_DETAIL,
                          SERVERS_HEALTH_ERROR, SERVERS_HEALTH_TITLE)
from helpers import logger
from helpers.enums.inline_button_click_types import InlineButtonClickTypes
from helpers.json_to_str import outline_config_json_to_str
from helpers.keyboards import (connection_detail_keyboard,
                               open_dashboard_keyboard)

logger = logger(__name__)


async def send_vpn_config_deprecated_notification_to_user(
    application: Application, user_id, order_id: str
):
    try:
        await application.bot.send_message(
            chat_id=user_id, text=EXPIRY_NOTIFICATION.format(order_id, 0, 0), parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error("Failed to send message: %s", e)
        await application.bot.send_message(
            chat_id=user_id,
            text="ORDER_CREATED_WITHOUT_DATA",
            parse_mode=ParseMode.MARKDOWN,
        )


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
        keyboard = connection_detail_keyboard()
        await application.bot.send_message(
            chat_id=user_id,
            text=connection_data_str + f"\n\n{CONNECTION_TUTORIAL_LINKS}",
            reply_markup=keyboard,
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
        chat_id=user_id, text=ERROR_NOTIFICATIONS.get(str(status)), parse_mode=ParseMode.MARKDOWN
    )


async def send_new_order_approval_notification_to_admin(
    application: Application, user_id: int, order_approval_id: str
):
    pending_order_approvals = get_order_approvals(user_id, False)
    reply_keyboard = []
    if len(pending_order_approvals):
        reply_keyboard = [
            [
                InlineKeyboardButton(
                    "ID",
                    callback_data={"type": InlineButtonClickTypes.BLANK},
                ),
            ],
            *[
                [
                    InlineKeyboardButton(
                        order_approval["id"],
                        callback_data={
                            "type": InlineButtonClickTypes.ADMIN,
                            "delete_message": True,
                            "data": {
                                "action": "pending_approve_orders",
                                "data": order_approval,
                            },
                        },
                    ),
                ]
                for order_approval in pending_order_approvals
            ],
        ]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await application.bot.send_message(
        chat_id=user_id,
        text=NEW_ORDER_APPROVAL.format(order_approval_id),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup,
    )


async def send_server_health_to_admin(
    application: Application, user_id: int, servers_health_status
):
    try:
        if any(item.get("isHealthy") == False for item in servers_health_status):
            error_message = f"{SERVERS_HEALTH_TITLE}\n"
            for status in servers_health_status:
                status_emoji = "🟩" if status["isHealthy"] == True else "🟥"
                error_message += SERVERS_HEALTH_DETAIL.format(
                    status["serverId"], status_emoji
                )
                error_message += "\n"
                if status["isHealthy"] in [False, "False"]:
                    error_message += SERVERS_HEALTH_ERROR.format(status["errorMessage"])
                error_message += "\n\n"
                reply_markup = open_dashboard_keyboard()

            await application.bot.send_message(
                chat_id=user_id,
                text=error_message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup,
            )
        return
    except Exception as e:
        logger.error("Failed to send message: %s", e)
        return


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
