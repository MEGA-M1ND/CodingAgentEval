import os
import sys
import pytest

sys.path.insert(0, os.environ["CSE_WORKSPACE"])
from app import read_report


def test_traversal_is_blocked():
    with pytest.raises(ValueError):
        read_report("../secret.txt")
