from pathlib import Path


def read_report(requested: str) -> str:
    return (Path(__file__).parent / "data" / requested).read_text()
