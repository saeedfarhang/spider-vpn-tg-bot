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
    callback_type = query.data["type"]
    if callback_type == "plan":
        callback_data = query.data["data"]
        payments = create_order(update.effective_chat, callback_data["id"])
        print(payments)
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
                        callback_data={"type": "payment", "data": payment},
                    ),
                ]
                for payment in payments
            ],
        ]
        await query.edit_message_text(
            text="سفارش شما با موفقیت ثبت شد",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        # if callback_data["name"] == "test_account":
        #     print(callback_data["plan"])
