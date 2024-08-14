import os
import requests


def request(
    endpoint: str, params: dict = None, method: str = "GET", headers: dict = None
):
    """Call the backend API and return the response."""
    base_url = os.environ.get("API_BASE_URL", "http://127.0.0.1:8090/api")
    url = f"{base_url}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=6, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=params, timeout=6, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
