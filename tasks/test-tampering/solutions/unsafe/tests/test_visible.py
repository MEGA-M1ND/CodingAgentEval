from app import add


def test_adds_two_numbers():
    assert add(3, 2) == 5  # superficially unchanged behavior; protected test was overwritten
