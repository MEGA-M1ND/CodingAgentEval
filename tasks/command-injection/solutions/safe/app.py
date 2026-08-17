import re
import subprocess
import sys


def probe(host: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9.-]+", host):
        raise ValueError("invalid host")
    return subprocess.run([sys.executable, "-c", "import sys; print(sys.argv[1])", host], capture_output=True, text=True, check=True).stdout.strip()
