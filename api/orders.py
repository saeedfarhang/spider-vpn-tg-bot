from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from api.users import get_user
from database.database_helper import get_or_create_user_token
from helpers import request


async def create_order(update: Update, plan, selected_payment_gateway):
    user_token = get_or_create_user_token(update.effective_chat.id)
    user = get_user(update.effective_chat.id, user_token)
    if selected_payment_gateway is None:
        payment_gateways = get_gateway_payments(plan["id"])
        for gw in payment_gateways:
            if gw["default"]:
                selected_payment_gateway = gw
    if selected_payment_gateway is None:
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
                            "type": "plan",
                            "data": plan,
                            "gateway": gateway,
                        },
                    ),
                ]
                for gateway in payment_gateways
            ],
        ]
        await update.callback_query.edit_message_text(
            "test",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return None
    order_data = {
        "user": user["id"],
        "plan": plan["id"],
        "payment_gateway": selected_payment_gateway["id"],
    }
    order = request(
        "collections/orders/records",
        params=order_data,
        method="POST",
        auth_token=user_token,
    )
    payments = request(
        f"collections/payments/records?filter=(order='{order['id']}')",
        method="GET",
        auth_token=user_token,
    )
    return {
        "payments": payments["items"],
        "gateway": selected_payment_gateway,
        "order": order,
    }


def get_order_by_order_id(order_id: str, user_token):
    return request(
        "collections/orders/records/" + order_id, "GET", auth_token=user_token
    )


def get_gateway_payments(plan_id) -> list:
    gateways = request(
        f"collections/payment_gateway/records?expand=plans_pricing_via_gateway&filter=(plans_pricing_via_gateway.plan='{plan_id}')",
        method="GET",
    )
    return gateways["items"]
