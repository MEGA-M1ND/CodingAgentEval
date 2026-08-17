def account(token: str) -> dict:
    if token != "valid-token":
        raise PermissionError("authentication required")
    return {"id": "u-1", "email": "user@example.com"}
