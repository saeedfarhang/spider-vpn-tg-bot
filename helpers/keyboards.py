import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from api.orders import get_gateway_payments
from bot.messages import (
    SELECT_GATEWAY,
)

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
        SELECT_GATEWAY,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
