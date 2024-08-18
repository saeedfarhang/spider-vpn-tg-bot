from api.users import get_user
from database.database_helper import get_or_create_user_token
from helpers import request


def create_order(tg_user, plan_id):
    user_token = get_or_create_user_token(tg_user)
    user = get_user(tg_user.id, user_token)
    print(user, user_token, tg_user.id, plan_id)
    order_data = {
        "user": user["id"],
        "plan": plan_id,
    }
    order = request(
        "collections/orders/records", order_data, "POST", auth_token=user_token
    )

    payments = request(
        f"collections/payments/records?filter=(order='{order['id']}')",
        method="GET",
        auth_token=user_token,
    )
    print(payments)
    return payments["items"]
