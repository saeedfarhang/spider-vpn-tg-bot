from telegram import Update

from api.users import get_user
from helpers import request


async def create_order(update: Update, plan, selected_payment_gateway):
    user_id = update.effective_chat.id
    user = get_user(update.effective_chat.id, user_id, update.effective_chat)
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
    # Step 1: Get plans_pricing records that match the given plan_id
    pricing_links = request(
        f"collections/plans_pricing/records?filter=(plan='{plan_id}')",
        method="GET"
    )["items"]

    # Step 2: Extract the unique gateway IDs from the matching records
    gateway_ids = set(p["gateway"] for p in pricing_links)

    if not gateway_ids:
        return []

    # Step 3: Query payment_gateway records using the gateway IDs
    # Build a filter like: (id='id1' || id='id2' || ...)
    filter_expr = " || ".join([f"(id='{gid}')" for gid in gateway_ids])
    gateways = request(
        f"collections/payment_gateway/records?filter={filter_expr}&expand=plans_pricing_via_gateway",
        method="GET"
    )

    return gateways["items"]
