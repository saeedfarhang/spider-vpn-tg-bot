from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from api.users import get_user
from database.database_helper import get_or_create_user_token
from helpers import request


async def create_order(update: Update, plan, selected_payment_gateway):
    user_id = update.effective_chat.id
    user = get_user(update.effective_chat.id, user_id)
    order_data = {
        "user": user["id"],
        "plan": plan["id"],
        "payment_gateway": selected_payment_gateway["id"],
    }
    order = request(
        "collections/orders/records",
        params=order_data,
        method="POST",
        user_id=user_id,
    )
    if order is not None:
        payments = request(
            f"collections/payments/records?filter=(order='{order['id']}')",
            method="GET",
            user_id=user_id,
        )
        return {
            "payments": payments["items"],
            "gateway": selected_payment_gateway,
            "order": order,
        }
    return None


def get_order_by_id(order_id: str, user_id):
    return request(
        "collections/orders/records/" + order_id + "?expand=vpn_config",
        user_id=user_id,
    )


def get_my_orders_by_status(status: str, user_id):
    res = request(
        f"collections/orders/records?filter=(status='{status}')&expand=vpn_config",
        "GET",
        user_id=user_id,
    )
    return res.get("items", [])


def get_gateway_payments(plan_id) -> list:
    gateways = request(
        f"collections/payment_gateway/records?expand=plans_pricing_via_gateway&filter=(plans_pricing_via_gateway.plan='{plan_id}')",
        method="GET",
    )
    return gateways["items"]
