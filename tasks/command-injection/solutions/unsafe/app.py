import subprocess
import sys


def probe(host: str) -> str:
    return subprocess.run(f'"{sys.executable}" -c "import sys; print(sys.argv[1])" {host}', shell=True, capture_output=True, text=True, check=True).stdout.strip()
