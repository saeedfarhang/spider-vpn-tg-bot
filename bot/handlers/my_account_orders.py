from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from api.orders import get_my_orders_by_status
from bot.messages import MY_ACCOUNT_ORDERS
from database.database_helper import get_or_create_user_token
from helpers import build_keyboard


async def my_account_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_token = get_or_create_user_token(user.id)

    orders = get_my_orders_by_status("COMPLETE", user_token)
    reply_keyboard = [
        [
            InlineKeyboardButton(
                "ظرفیت",
                callback_data={"type": "blank"},
            ),
            InlineKeyboardButton(
                "شماره سفارش",
                callback_data={"type": "blank"},
            ),
        ],
        *[
            [
                InlineKeyboardButton(
                    f"{order['expand']['vpn_config']['usage_in_gb']} GB / روزه {order['expand']['vpn_config']['usage_in_gb']}",
                    callback_data={"type": "order", "data": order},
                ),
                InlineKeyboardButton(
                    (order["id"]),
                    callback_data={
                        "type": "order",
                        "data": order,
                        "show_keyboard": True,
                    },
                ),
            ]
            for order in orders
        ],
    ]

    await build_keyboard(update, MY_ACCOUNT_ORDERS, reply_keyboard, False)
