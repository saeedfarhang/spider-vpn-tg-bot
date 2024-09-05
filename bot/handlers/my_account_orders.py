from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from api.orders import get_my_orders_by_status
from bot.buttons import test_account_button_with_callback
from bot.messages import MY_ACCOUNT_ORDERS, MY_ACCOUNT_ORDERS_NOT_FOUND
from helpers import build_keyboard
from helpers.enums.inline_button_click_types import InlineButtonClickTypes


async def my_account_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    orders = get_my_orders_by_status("COMPLETE", user.id)
    reply_keyboard = []
    text = MY_ACCOUNT_ORDERS_NOT_FOUND
    if len(orders):
        text = MY_ACCOUNT_ORDERS
        reply_keyboard = [
            [
                InlineKeyboardButton(
                    "ظرفیت",
                    callback_data={"type": InlineButtonClickTypes.BLANK},
                ),
                InlineKeyboardButton(
                    "شماره سفارش",
                    callback_data={"type": InlineButtonClickTypes.BLANK},
                ),
            ],
            *[
                [
                    InlineKeyboardButton(
                        f"{order['expand']['vpn_config']['usage_in_gb']} GB / روزه {order['expand']['vpn_config']['usage_in_gb']}",
                        callback_data={
                            "type": InlineButtonClickTypes.ORDER,
                            "data": order,
                        },
                    ),
                    InlineKeyboardButton(
                        (order["id"]),
                        callback_data={
                            "type": InlineButtonClickTypes.ORDER,
                            "data": order,
                            "show_keyboard": True,
                        },
                    ),
                ]
                for order in orders
            ],
        ]
    else:
        test_account_button = test_account_button_with_callback(
            callback_data={"type": InlineButtonClickTypes.TEST_ACCOUNT}
        )
        reply_keyboard = [[test_account_button[0]]]
    await build_keyboard(update, text, reply_keyboard, False)
