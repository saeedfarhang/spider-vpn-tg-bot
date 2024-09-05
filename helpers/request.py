import os
import requests

from api.webhook import notify_error
from database.database_helper import get_or_create_user_token


def request(
    endpoint: str,
    params: dict = None,
    files: dict = None,
    method: str = "GET",
    headers: dict = {"content-type": "application/json"},
    user_id: str = None,
    call_webhook: bool = False,
):
    """Call the backend API and return the response."""
    if call_webhook:
        host = os.environ.get("WEBHOOK_HOST", "localhost")
        port = str(os.environ.get("WEBHOOK_PORT", 5000))
        base_url = "http://" + host + ":" + port
    else:
        base_url = os.environ.get("API_BASE_URL", "http://127.0.0.1:8090/api")
    url = f"{base_url}/{endpoint}"
    if user_id:
        user_token = get_or_create_user_token(user_id)
        headers_with_auth = {
            **headers,
            "Authorization": f"Bearer {user_token}",
        }
    else:
        headers_with_auth = {
            **headers,
            "Authorization": None,
        }
    try:
        if method == "GET":
            response = requests.get(
                url, params=params, timeout=20, headers=headers_with_auth
            )
        elif method == "POST" and files:
            response = requests.request(
                "POST",
                url,
                headers=headers_with_auth,
                data=params,
                files=files,
                timeout=20,
            )
        elif method == "POST":
            response = requests.post(
                url, json=params, timeout=20, headers=headers_with_auth
            )
        elif method == "DELETE":
            response = requests.delete(
                url, json=params, timeout=20, headers=headers_with_auth
            )
        elif method == "PUT":
            response = requests.put(
                url, json=params, timeout=20, headers=headers_with_auth
            )
        elif method == "PATCH":
            response = requests.patch(
                url, json=params, timeout=20, headers=headers_with_auth
            )
        else:
            raise ValueError("Unsupported HTTP method")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        print(e.response)
        notify_error(user_id, e.response.status_code)
        print(f"API request failed: {e}")
        return None
