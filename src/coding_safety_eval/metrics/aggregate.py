from __future__ import annotations

from collections.abc import Iterable
from statistics import mean

from coding_safety_eval.models.result import EvaluationResult


def aggregate(results: Iterable[EvaluationResult | dict]) -> dict[str, float | int]:
    rows = [r.to_dict() if isinstance(r, EvaluationResult) else r for r in results]
    count = len(rows)
    if not count:
        return {"runs": 0}
    rate = lambda key: round(sum(bool(row[key]) for row in rows) / count * 100, 1)
    return {"runs": count, "functional_success_rate": rate("functional_pass"), "security_success_rate": rate("security_pass"), "safe_success_rate": rate("overall_success"), "false_success_rate": round(sum(row["classification"] == "FALSE_SUCCESS" for row in rows) / count * 100, 1), "integrity_violation_rate": round(sum(not row["integrity_pass"] for row in rows) / count * 100, 1), "mean_steps": round(mean(row["steps"] for row in rows), 2), "mean_latency_seconds": round(mean(row["duration_seconds"] for row in rows), 3)}
