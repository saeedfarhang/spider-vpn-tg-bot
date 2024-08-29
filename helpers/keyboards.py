import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from telegram.constants import ParseMode
from api.order_approval import create_order_approval
from api.orders import create_order, get_gateway_payments, get_order_by_id
from database.database_helper import get_or_create_user_token
from helpers.json_to_str import outline_config_json_to_str

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def build_keyboard(
    update: Update, message: str, keyboard, resize_keyboard: bool
) -> None:
    """Helper function to build the next inline keyboard."""

    if resize_keyboard:
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=resize_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the menu to the user
    await update.message.reply_text(message, reply_markup=reply_markup)

    return


async def approve_pending_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"tmp/order_approval/{photo_file.file_unique_id}.jpg"
    await photo_file.download_to_drive(photo_path)

    user_token = get_or_create_user_token(update.effective_chat.id)
    if order_id := context.user_data.get("order_id"):
        get_order_by_id(order_id, user_token)
        await create_order_approval(photo_path, order_id, user_token)

    await update.message.reply_text(text=WAIT_FOR_APPROVE)


async def select_plan(update: Update, plan):
    selected_payment_gateway = None
    payment_gateways = get_gateway_payments(plan["id"])
    for gw in payment_gateways:
        if gw["default"]:
            selected_payment_gateway = gw
    keyboard = [
        [
            InlineKeyboardButton(
                "روش پرداخت",
                callback_data={"type": "blank"},
            ),
        ],
        *[
            [
                InlineKeyboardButton(
                    f'{gateway["name"]}',
                    callback_data={
                        "type": "gateway",
                        "data": plan,
                        "gateway": gateway,
                    },
                ),
            ]
            for gateway in payment_gateways
        ],
    ]

    await update.callback_query.message.reply_text(
        "test",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return selected_payment_gateway


async def button_click_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This Python async function handles different actions based on the callback type received from a
    button click in a Telegram bot.

    :param update: The `update` parameter in the `button_click_callback` function is an object that
    contains information about the incoming update from the user. It typically includes details such as
    the user's message, callback query, or inline query
    :type update: Update
    :param context: The `context` parameter in the `button_click_callback` function is of type
    `ContextTypes.DEFAULT_TYPE`. This parameter is used to pass contextual information and data between
    different parts of the code within the Telegram bot application. It allows you to access
    user-specific data, bot settings, and other relevant information
    :type context: ContextTypes.DEFAULT_TYPE
    :return: The function `button_click_callback` is returning None.
    """
    query = update.callback_query
    await query.answer()
    callback_type = query.data["type"]
    callback_data: dict = None
    order_id = None
    if query.data:
        callback_data = query.data["data"]

    edit_messages = {
        "plan": EDIT_SELECT_PLAN_MESSAGE.format(
            callback_data.get("common_name", "no name")
        )
    }

    if edit_message := edit_messages.get(callback_type, None):
        await query.edit_message_text(text=edit_message, parse_mode=ParseMode.MARKDOWN)
    else:
        await query.edit_message_reply_markup(None)
    selected_payment_gateway = None
    print("\n\n\nhere is also", callback_type, callback_data)
    if callback_type == "plan":
        selected_payment_gateway = await select_plan(update, callback_data)
    elif callback_type == "gateway":
        if selected_payment_gateway is None:
            selected_payment_gateway = query.data["gateway"]
        data = await create_order(update, callback_data, selected_payment_gateway)
        print("\n\n\nhere is: ", selected_payment_gateway, callback_type, data)
        if data is not None:
            order_id = data["order"]["id"] if data else order_id
            print("order_id changed", order_id)
            context.user_data["order_id"] = order_id

        if data and data["payments"]:
            if data["gateway"]["type"] == "FREE":
                await query.message.reply_text(
                    text=data["gateway"]["data"], parse_mode=ParseMode.MARKDOWN
                )
            else:
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "روش پرداخت",
                            callback_data={"type": "blank"},
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
                text="سفارش شما با موفقیت ثبت شد",
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
            text=outline_config_json_to_str(COMPLETE_ORDER_HEAD_TEXT, callback_data),
            parse_mode=ParseMode.MARKDOWN,
        )

    elif callback_type == "blank":
        pass
