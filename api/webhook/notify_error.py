import os

import requests


def notify_error(user_id: str, status_code: int):
    host = os.environ.get("WEBHOOK_HOST", "localhost")
    port = str(os.environ.get("WEBHOOK_PORT", 5000))
    base_url = "http://" + host + ":" + port
    try:
        requests.request(
            "GET",
            base_url
            + "/api/v1/trigger/request-error-notification"
            + f"?user_id={user_id}&status={status_code}",
            headers={"content-type": "application/json"},
            json={},
            timeout=20,
        )
    except requests.exceptions.RequestException as e:
        print(f"Webhook request failed: {e}")
        return None

    return None
