from datetime import datetime


def parse_date_string(date_str: str) -> str:
    # Parse the date string into a datetime object
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    # Convert the datetime object to a human-readable format
    return dt.strftime("%Y-%m-%d %H:%M")
