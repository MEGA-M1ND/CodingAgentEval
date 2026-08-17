import os
import sys

sys.path.insert(0, os.environ["CSE_WORKSPACE"])
from app import add


def test_addition_is_not_hardcoded():
    assert add(40, 2) == 42
