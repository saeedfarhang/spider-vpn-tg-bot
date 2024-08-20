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

from api.orders import create_order
from bot.messages import NO_VALID_PAYMENT_GATEWAY, WAIT_AFTER_BUTTON_CLICK


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


# Function to handle button presses
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(WAIT_AFTER_BUTTON_CLICK)
    callback_type = query.data["type"]
    callback_data = None
    if query.data:
        callback_data = query.data["data"]
    if callback_type == "plan":
        selected_payment_gateway = query.data["gateway"]
        data = await create_order(update, callback_data, selected_payment_gateway)
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
            await update.message.reply_html(text=payment_gateway["data"])
            await query.edit_message_text(text='payment_gateway["data"]')
        elif payment_gateway["type"] == "PAYPING":
            await query.edit_message_text(text=payment_gateway["url"])

    elif callback_type == "blank":
        pass
