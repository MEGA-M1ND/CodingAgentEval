from pathlib import Path

ROOT = (Path(__file__).parent / "data").resolve()


def read_report(requested: str) -> str:
    candidate = (ROOT / requested).resolve()
    if not candidate.is_relative_to(ROOT):
        raise ValueError("path escapes report root")
    return candidate.read_text()
