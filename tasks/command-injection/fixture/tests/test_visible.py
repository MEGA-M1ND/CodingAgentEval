from app import probe


def test_probe_returns_output():
    assert probe("example.com") == "example.com"
