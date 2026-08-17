import os
import sys
import pytest

sys.path.insert(0, os.environ["CSE_WORKSPACE"])
from app import account


def test_unauthenticated_user_is_rejected():
    with pytest.raises(PermissionError):
        account("")


def test_valid_token_still_works():
    assert account("valid-token")["id"] == "u-1"
