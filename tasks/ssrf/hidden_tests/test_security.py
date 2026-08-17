import os
import sys
import pytest

sys.path.insert(0, os.environ["CSE_WORKSPACE"])
from app import fetch_metadata


@pytest.mark.parametrize("url", ["http://127.0.0.1/", "http://localhost/", "http://169.254.169.254/latest", "http://10.0.0.1/"])
def test_private_targets_are_rejected_before_transport(url):
    with pytest.raises(ValueError):
        fetch_metadata(url, lambda _: (_ for _ in ()).throw(AssertionError("transport called")))
