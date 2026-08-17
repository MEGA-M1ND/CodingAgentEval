"""Render actual stored benchmark results; it never fabricates rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from coding_safety_eval.metrics.aggregate import aggregate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    args = parser.parse_args()
    rows = [json.loads(path.read_text()) for path in args.results.glob("**/result.json")]
    if not rows:
        raise SystemExit("No result.json files found; pass one execution directory.")
    print("Task\tFunctional\tSecurity\tIntegrity\tSafe Success\tClassification")
    for row in sorted(rows, key=lambda item: item["task_id"]):
        flag = lambda value: "PASS" if value else "FAIL"
        print(f"{row['task_id']}\t{flag(row['functional_pass'])}\t{flag(row['security_pass'])}\t{flag(row['integrity_pass'])}\t{flag(row['overall_success'])}\t{row['classification']}")
    for key, value in aggregate(rows).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
