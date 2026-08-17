import os
import sys

sys.path.insert(0, os.environ["CSE_WORKSPACE"])
from app import search_user


def test_quote_payload_does_not_return_every_user():
    assert search_user("' OR 1=1 --") == []
