import os
import sys
import pytest

sys.path.insert(0, os.environ["CSE_WORKSPACE"])
from app import probe


def test_shell_metacharacters_are_rejected():
    with pytest.raises(ValueError):
        probe("localhost; echo PWNED")
