import logging
from bot.handlers import test_account
from helpers.json_to_str import outline_config_json_to_str

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from telegram.constants import ParseMode
from api.orders import create_order
from bot.messages import (
    CREATE_ORDER_FACTOR,
    EDIT_SELECT_PLAN_MESSAGE,
    GET_ORDER_HEAD_TEXT,
    NO_VALID_PAYMENT_GATEWAY,
)
from helpers.json_to_str import outline_config_json_to_str
from helpers.keyboards import select_plan

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
            "plan": EDIT_SELECT_PLAN_MESSAGE.format(
                callback_data.get("common_name", "no name")
            ),
        }

        if edit_message := edit_messages.get(callback_type, None):
            await query.edit_message_text(
                text=edit_message, parse_mode=ParseMode.MARKDOWN
            )
        elif query.data.get("show_keyboard", False) is False:
            await query.edit_message_reply_markup(None)

        selected_payment_gateway = None
    if callback_type == "plan":
        selected_payment_gateway = await select_plan(update, callback_data)
        if selected_payment_gateway is not None:
            callback_type = "gateway"
    if callback_type == "gateway":
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
                                "type": "payment",
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
                                    "type": "payment",
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
                )
        elif data and data["payments"] == []:
            await query.message.reply_text(
                text=NO_VALID_PAYMENT_GATEWAY,
            )
    elif callback_type == "payment":
        payment_gateway = callback_data["gateway"]
        if payment_gateway["type"] == "FREE":
            await query.message.reply_text(
                text=payment_gateway["data"], parse_mode=ParseMode.HTML
            )
        if payment_gateway["type"] == "ADMIN_APPROVE":
            await query.message.reply_text(
                text=payment_gateway["data"], parse_mode=ParseMode.HTML
            )

            return
        if payment_gateway["type"] == "PAYPING":
            await query.message.reply_text(text=payment_gateway["url"])
    elif callback_type == "order":
        logger.debug("callback_data: %c", callback_data)
        await query.message.reply_text(
            text=outline_config_json_to_str(
                GET_ORDER_HEAD_TEXT.format(callback_data.get("id", "N/A")),
                callback_data,
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    elif callback_type == "test_account":
        await test_account(update, context)
    elif callback_type == "blank":
        pass
