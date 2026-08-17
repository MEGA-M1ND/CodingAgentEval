from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Grade:
    passed: bool
    output: str = ""
    failures: list[str] = field(default_factory=list)
