from datetime import datetime
import sqlite3

from telegram import User

from api.auth import auth_refresh
from api.users import get_create_user_token


def create_table():
    conn = sqlite3.connect("user_tokens.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user_tokens (
            tg_user_id STRING PRIMARY KEY,
            token TEXT,
            updated_at DATETIME,
            is_admin BOOLEAN DEFAULT 0
        )
    """
    )
    conn.commit()
    conn.close()


def set_user_token(tg_user: User, token: str):
    """
    Updates or inserts a user token in a SQLite database based on the Telegram user ID,
    and updates the `updated_at` timestamp.
    """
    conn = sqlite3.connect("user_tokens.db")
    c = conn.cursor()
    current_time = datetime.now().isoformat()  # Use isoformat without extra formatting

    c.execute(
        "SELECT token, updated_at FROM user_tokens WHERE tg_user_id = ?", (tg_user.id,)
    )
    result = c.fetchone()
    if result:
        last_updated = datetime.fromisoformat(result[1])  # Parse using fromisoformat
        time_diff = datetime.now() - last_updated
        if time_diff.total_seconds() > 7200:  # 2 hours in seconds
            c.execute(
                "UPDATE user_tokens SET token=?, updated_at=? WHERE tg_user_id = ?",
                (token, current_time, tg_user.id),
            )
    else:
        c.execute(
            "INSERT INTO user_tokens (tg_user_id, token, updated_at) VALUES (?, ?, ?)",
            (tg_user.id, token, current_time),
        )
    conn.commit()
    conn.close()
    return token


def get_or_create_user_token(tg_user_id: str, USER_ADMIN_IDS: list = None):
    """
    Retrieves an existing user token from the database based on the Telegram user ID
    or creates a new token if it does not exist, handling token replacement if `updated_at`
    is older than 2 hours.
    """
    conn = sqlite3.connect("user_tokens.db")
    c = conn.cursor()
    current_time = datetime.now()  # Use datetime object directly for time comparisons

    c.execute(
        "SELECT token, updated_at FROM user_tokens WHERE tg_user_id = ?", (tg_user_id,)
    )
    result = c.fetchone()
    if result:
        last_updated = datetime.fromisoformat(result[1])  # Parse using fromisoformat
        time_diff = current_time - last_updated
        if time_diff.total_seconds() <= 7200:
            return result[0]
        else:
            c.execute("DELETE FROM user_tokens WHERE tg_user_id = ?", (tg_user_id,))

    is_admin = tg_user_id in USER_ADMIN_IDS if USER_ADMIN_IDS else []
    token = get_create_user_token(tg_user_id)
    c.execute(
        "INSERT INTO user_tokens (tg_user_id, token, updated_at, is_admin) VALUES (?, ?, ?, ?)",
        (
            tg_user_id,
            token,
            current_time.isoformat(),
            is_admin,
        ),  # Store as ISO format string
    )
    conn.commit()
    conn.close()
    return token


create_table()
