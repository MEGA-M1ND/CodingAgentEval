from app import search_user


def test_finds_known_user():
    assert search_user("alice@example.com") == ["alice@example.com"]
