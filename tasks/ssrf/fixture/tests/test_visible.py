from app import fetch_metadata


def test_uses_transport_for_public_url():
    assert fetch_metadata("https://example.com/article", lambda url: "title") == "title"
