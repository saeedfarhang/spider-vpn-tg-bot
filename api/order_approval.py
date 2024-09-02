import requests
from telegram import File
from helpers import request


async def create_order_approval(
    photo_path: str, photo_id: str, order: str, user_id=str
):
    data = {"order": order, "photo_tg_id": photo_id}
    files = [
        (
            "photo",
            (
                photo_path,
                open(
                    photo_path,
                    "rb",
                ),
                "image/jpeg",
            ),
        )
    ]
    return request(
        "collections/order_approval/records",
        params=data,
        files=files,
        headers={},
        method="POST",
        user_id=user_id,
    )


def get_order_approvals(user_id: str, is_approved: bool):
    res = request(
        f"collections/order_approval/records?filter=(is_approved={is_approved})",
        {},
        method="GET",
        user_id=user_id,
    )
    return res.get("items", [])


def approve_order_approval(user_id: str, order_approval_id: str):
    data = {"is_approved": True}
    res = request(
        f"collections/order_approval/records/{order_approval_id}",
        data,
        method="PATCH",
        user_id=user_id,
    )
    if res:
        return True
    return False


def detect_fraud_order_approval(user_id: str, order_approval_id: str):
    data = {"is_fraud": True}
    res = request(
        f"collections/order_approval/records/{order_approval_id}",
        data,
        method="PATCH",
        user_id=user_id,
    )
    if res:
        return True
    return False
