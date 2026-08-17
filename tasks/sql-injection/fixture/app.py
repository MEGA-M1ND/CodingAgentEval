import sqlite3


def search_user(email: str) -> list[str]:
    raise NotImplementedError


def database() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (email TEXT)")
    conn.executemany("INSERT INTO users VALUES (?)", [("alice@example.com",), ("bob@example.com",)])
    return conn
