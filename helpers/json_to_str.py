from flask import json


def json_to_str(json_data: dict) -> str:
    # Initialize the table with the headers
    headers = ["Key", "Value"]
    rows = []

    # Iterate through the dictionary items
    for key, value in json_data.items():
        # Handle nested dictionaries
        if isinstance(value, dict):
            value = json_to_str(value)  # Recursively convert nested dictionary
        # Handle lists (for example, if any list needs to be formatted)
        elif isinstance(value, list):
            value = "\n".join(map(str, value))
        rows.append(f"| {key} | {value} |")

    # Create the separator row
    separator = "| --- | --- |"

    # Construct the Markdown table
    table = "\n".join([f"| {headers[0]} | {headers[1]} |", separator, "\n".join(rows)])

    return table


def outline_config_json_to_str(json_data: dict):
    print(json_data)
    return f"""
اتصال عنکبوت شما ایجاد شد. 
لینک اتصال: 
{json_data['accessUrl']}
"""
