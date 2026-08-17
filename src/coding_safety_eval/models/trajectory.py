"""Observable JSONL trajectory logging; no model reasoning is collected."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class Trajectory:
    run_id: str
    task_id: str
    events: list[dict[str, Any]] = field(default_factory=list)

    def log(self, event: str, **data: Any) -> None:
        self.events.append({"timestamp": datetime.now(UTC).isoformat(), "event": event, **data})

    def write_jsonl(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(json.dumps(event, sort_keys=True) for event in self.events) + "\n", encoding="utf-8")
