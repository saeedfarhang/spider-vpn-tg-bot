import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from api.orders import get_gateway_payments
from bot.messages import SELECT_GATEWAY
from helpers.enums.inline_button_click_types import InlineButtonClickTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def select_plan(update: Update, plan):
    selected_payment_gateway = None
    payment_gateways = get_gateway_payments(plan["id"])
    if len(payment_gateways) == 1:
        selected_payment_gateway = payment_gateways[0]
    else:
        for gw in payment_gateways:
            if gw["default"]:
                selected_payment_gateway = gw
                break
    if selected_payment_gateway is not None:
        return selected_payment_gateway
    keyboard = [
        [
            InlineKeyboardButton(
                "درگاه پرداخت",
                callback_data={"type": InlineButtonClickTypes.BLANK},
            ),
        ],
        *[
            [
                InlineKeyboardButton(
                    f'{gateway["name"]}',
                    callback_data={
                        "type": InlineButtonClickTypes.GATEWAY,
                        "data": plan,
                        "gateway": gateway,
                    },
                ),
            ]
            for gateway in payment_gateways
        ],
    ]

    await update.callback_query.message.reply_text(
        SELECT_GATEWAY,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def connection_detail_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "راهنمای اتصال",
                callback_data={"type": InlineButtonClickTypes.HOW_TO_CONNECT},
            ),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def open_dashboard_keyboard():   
    dashboard_url = os.environ.get(
                "DASHBOARD_URL", "http://localhost:8090/_"
            )
    keyboard = [
        [
            InlineKeyboardButton(
                "باز کردن داشبورد",
                url=dashboard_url,
            ),
        ]
        # http://localhost:8090/_/#/collections?collectionId=hb3m9ybn0gnjbk9&filter=v0hyj09f5b8dg5a&sort=-created&recordId=v0hyj09f5b8dg5a
    ]
    return InlineKeyboardMarkup(keyboard)


def sponsor_channels_keyboard(channel_ids: list[str]):
    keyboard = [
        [
            *[
                InlineKeyboardButton(
                    "کانال " + channel_id, url="https://t.me/" + channel_id[1:]
                )
                for channel_id in channel_ids
            ]
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
