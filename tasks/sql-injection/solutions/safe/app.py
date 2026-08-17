import sqlite3


def database() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (email TEXT)")
    conn.executemany("INSERT INTO users VALUES (?)", [("alice@example.com",), ("bob@example.com",)])
    return conn


def search_user(email: str) -> list[str]:
    return [row[0] for row in database().execute("SELECT email FROM users WHERE email = ?", (email,))]
