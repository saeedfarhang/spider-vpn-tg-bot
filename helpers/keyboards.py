from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ContextTypes,
)

from api.order_approval import create_order_approval
from api.orders import create_order, get_order_by_order_id
from bot.messages import (
    NO_VALID_PAYMENT_GATEWAY,
    WAIT_AFTER_BUTTON_CLICK,
    WAIT_FOR_APPROVE,
)
from bot.state import PAYMENT_APPROVE
from database.database_helper import get_or_create_user_token


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
        get_order_by_order_id(order_id, user_token)
        await create_order_approval(photo_path, order_id, user_token)

    await update.message.reply_text(text=WAIT_FOR_APPROVE)


# Function to handle button presses
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(WAIT_AFTER_BUTTON_CLICK)
    callback_type = query.data["type"]
    callback_data = None
    order_id = None
    if query.data:
        callback_data = query.data["data"]
    if callback_type == "plan":
        selected_payment_gateway = query.data["gateway"]
        data = await create_order(update, callback_data, selected_payment_gateway)
        order_id = data["order"]["id"] if data else order_id
        print("order_id changed", order_id)
        context.user_data["order_id"] = order_id

        if data and data["payments"]:
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
            await query.edit_message_text(
                text="سفارش شما با موفقیت ثبت شد",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        elif data and data["payments"] == []:
            await query.edit_message_text(
                text=NO_VALID_PAYMENT_GATEWAY,
            )
    elif callback_type == "payment":
        payment_gateway = callback_data["gateway"]
        if payment_gateway["type"] == "ADMIN_APPROVE":
            await update.callback_query.message.reply_text(
                text=payment_gateway["data"], parse_mode="Html"
            )
            await query.edit_message_text(
                text=payment_gateway["data"], parse_mode="Html"
            )

            return
        if payment_gateway["type"] == "PAYPING":
            await query.edit_message_text(text=payment_gateway["url"])

    elif callback_type == "blank":
        pass
