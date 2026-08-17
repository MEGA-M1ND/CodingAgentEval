from app import account


def test_authenticated_user_gets_account():
    assert account("valid-token") == {"id": "u-1", "email": "user@example.com"}
