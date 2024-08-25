import requests
from telegram import File
from helpers import request


async def create_order_approval(photo_path: str, order: str, auth_token=str):
    data = {"order": order}
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
        auth_token=auth_token,
    )
