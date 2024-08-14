import sqlite3

from telegram import User

from helpers.api.auth import auth_refresh
from helpers.api.users import get_create_user_token


def create_table():
    conn = sqlite3.connect("user_tokens.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user_tokens (
            chat_id INTEGER PRIMARY KEY,
            token TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def get_or_create_user_token(tg_user: User | None):
    conn = sqlite3.connect("user_tokens.db")
    c = conn.cursor()
    c.execute("SELECT token FROM user_tokens WHERE chat_id = ?", (tg_user.id,))
    result = c.fetchone()
    if result:
        token = result[0]
        if new_token := auth_refresh(token):
            c.execute(
                "UPDATE user_tokens SET  token=? WHERE ?",
                (tg_user.id, new_token["token"]),
            )
            conn.close()
            return new_token["token"]
        c.execute(
            "DELETE FROM user_tokens WHERE chat_id = ?",
            (tg_user.id,),
        )
    token = get_create_user_token(tg_user)
    c.execute(
        "INSERT INTO user_tokens (chat_id, token) VALUES (?, ?)",
        (tg_user.id, token),
    )
    conn.commit()
    conn.close()
    return token


create_table()
