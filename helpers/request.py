import os
import requests


def request(
    endpoint: str,
    params: dict = None,
    files: dict = None,
    method: str = "GET",
    headers: dict = {"content-type": "application/json"},
    auth_token: str = None,
):
    """Call the backend API and return the response."""
    base_url = os.environ.get("API_BASE_URL", "http://127.0.0.1:8090/api")
    url = f"{base_url}/{endpoint}"
    headers_with_auth = {
        **headers,
        "Authorization": auth_token,
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
        else:
            raise ValueError("Unsupported HTTP method")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
