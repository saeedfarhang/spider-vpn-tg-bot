import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from api.order_approval import (approve_order_approval,
                                detect_fraud_order_approval)
from api.orders import create_order
from bot.handlers.admin.get_pending_approve_orders import (
    get_pending_approve_order_by_data, get_pending_approve_orders)
from bot.handlers.how_to_connect import (how_to_connect,
                                         how_to_connect_data_callback)
from bot.handlers.test_account import test_account
from bot.messages import (CONNECTION_TUTORIAL_LINKS, CREATE_ORDER_FACTOR,
                          EDIT_SELECT_PLAN_MESSAGE, GET_ORDER_HEAD_TEXT,
                          NO_VALID_PAYMENT_GATEWAY,
                          ORDER_APPROVAL_APPROVED_SUCCESSFUL,
                          ORDER_APPROVAL_DETECT_FRAUD_SUCCESSFUL)
from helpers.enums.inline_button_click_types import InlineButtonClickTypes
from helpers.json_to_str import outline_config_json_to_str
from helpers.keyboards import connection_detail_keyboard, select_plan

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def inline_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This Python async function handles different actions based on the callback type received from a
    button click in a Telegram bot.

    :param update: The `update` parameter in the `inline_button_click` function is an object that
    contains information about the incoming update from the user. It typically includes details such as
    the user's message, callback query, or inline query
    :type update: Update
    :param context: The `context` parameter in the `inline_button_click` function is of type
    `ContextTypes.DEFAULT_TYPE`. This parameter is used to pass contextual information and data between
    different parts of the code within the Telegram bot application. It allows you to access
    user-specific data, bot settings, and other relevant information
    :type context: ContextTypes.DEFAULT_TYPE
    :return: The function `inline_button_click` is returning None.
    """
    query = update.callback_query
    await query.answer()
    callback_type = query.data["type"]
    callback_data: dict = None
    order_id = None
    if query.data:
        callback_data = query.data.get("data", None)

    if callback_data:
        edit_messages = {
            InlineButtonClickTypes.PLAN: EDIT_SELECT_PLAN_MESSAGE.format(
                callback_data.get("common_name", "no name")
            ),
        }
        if edit_message := edit_messages.get(callback_type, None):
            await query.edit_message_text(
                text=edit_message, parse_mode=ParseMode.MARKDOWN
            )
        elif query.data.get("show_keyboard", False) is False:
            await query.edit_message_reply_markup(None)
        elif query.data.get("delete_message", False):
            await query.delete_message()

        selected_payment_gateway = None
    if callback_type == InlineButtonClickTypes.PLAN:
        selected_payment_gateway = None
        if (int(callback_data.get("capacity", "0"))):
            selected_payment_gateway = await select_plan(update, callback_data)
        elif selected_payment_gateway is not None:
            callback_type = InlineButtonClickTypes.GATEWAY
    if callback_type == InlineButtonClickTypes.GATEWAY:
        if selected_payment_gateway is None:
            selected_payment_gateway = query.data["gateway"]
        data = await create_order(update, callback_data, selected_payment_gateway)
        if data is not None:
            order_id = data["order"]["id"] if data else order_id
            context.user_data["order_id"] = order_id

        if data and data["payments"]:
            if data["gateway"]["type"] == "FREE":
                text = data["gateway"].get("data", None)
                if text:
                    await query.message.reply_text(
                        text=data["gateway"]["data"], parse_mode=ParseMode.MARKDOWN
                    )

            elif len(data["payments"]):
                first_payment = data["payments"][0]

                keyboard = [
                    [
                        InlineKeyboardButton(
                            "تایید نهایی",
                            callback_data={
                                "type": InlineButtonClickTypes.PAYMENT,
                                "data": {
                                    "payment": first_payment,
                                    "gateway": data["gateway"],
                                },
                            },
                        ),
                    ],
                    *[
                        [
                            InlineKeyboardButton(
                                f'{payment["amount"]} {payment["currency"]}',
                                callback_data={
                                    "type": InlineButtonClickTypes.PAYMENT,
                                    "data": {
                                        "payment": payment,
                                        "gateway": data["gateway"],
                                    },
                                },
                            ),
                        ]
                        for payment in data["payments"]
                    ],
                ]
                await query.message.reply_text(
                    text=CREATE_ORDER_FACTOR.format(
                        str(first_payment["amount"])
                        + " "
                        + str(first_payment["currency"]),
                        data["gateway"]["name"],
                    ),
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN,
                )
        elif data and data["payments"] == []:
            await query.message.reply_text(
                text=NO_VALID_PAYMENT_GATEWAY,
            )
    elif callback_type == InlineButtonClickTypes.PAYMENT:
        payment_gateway = callback_data["gateway"]
        if payment_gateway["type"] == "FREE":
            await query.message.reply_text(
                text=payment_gateway["data"], parse_mode=ParseMode.HTML
            )
        if payment_gateway["type"] == "ADMIN_APPROVE":
            keyboard = None
            if payment_gateway.get("link", False):
                keyboard = [
                    [
                        InlineKeyboardButton("پرداخت", url=payment_gateway["link"]),
                    ],
                ]
            await query.message.reply_text(
                text=payment_gateway["data"],
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None,
            )
            return
        if payment_gateway["type"] == "PAYPING":
            await query.message.reply_text(text=payment_gateway["url"])
    elif callback_type == InlineButtonClickTypes.ORDER:
        logger.debug("callback_data: %c", callback_data)

        keyboard = connection_detail_keyboard()

        await query.message.reply_text(
            text=outline_config_json_to_str(
                GET_ORDER_HEAD_TEXT.format(callback_data.get("id", "N/A")),
                callback_data,
            )
            + f"\n\n{CONNECTION_TUTORIAL_LINKS}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard,
        )
    elif callback_type == InlineButtonClickTypes.TEST_ACCOUNT:
        await test_account(update, context)
    elif callback_type == InlineButtonClickTypes.HOW_TO_CONNECT:
        if callback_data and callback_data["platform"]:
            await how_to_connect_data_callback(query, callback_data["platform"])
        else:
            await how_to_connect(update, context)
    elif callback_type == InlineButtonClickTypes.BLANK:
        pass
    elif callback_type == InlineButtonClickTypes.ADMIN:
        callback_action = callback_data.get("action", "blank")
        if callback_action == "pending_approve_orders":
            if order_approval_data := callback_data.get("data", None):
                await get_pending_approve_order_by_data(update, order_approval_data)
            else:
                await get_pending_approve_orders(update)
        if callback_action == "approve_order_approval":
            if order_approval_data := callback_data.get("data", None):
                if approve_order_approval(
                    update.effective_chat.id, order_approval_data["id"]
                ):
                    await query.message.reply_text(
                        text=ORDER_APPROVAL_APPROVED_SUCCESSFUL,
                        parse_mode=ParseMode.MARKDOWN,
                    )
        elif callback_action == "detect_fraud_order_approval":
            if order_approval_data := callback_data.get("data", None):
                if detect_fraud_order_approval(
                    update.effective_chat.id, order_approval_data["id"]
                ):
                    await query.message.reply_text(
                        text=ORDER_APPROVAL_DETECT_FRAUD_SUCCESSFUL,
                        parse_mode=ParseMode.MARKDOWN,
                    )
