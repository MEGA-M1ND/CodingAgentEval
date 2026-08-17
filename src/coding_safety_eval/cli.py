from __future__ import annotations

import argparse
import json
from pathlib import Path

from coding_safety_eval.agents.manual_patch_agent import ManualPatchAgent
from coding_safety_eval.agents.openrouter_agent import OpenRouterAgent
from coding_safety_eval.metrics.aggregate import aggregate
from coding_safety_eval.models.task import discover_tasks
from coding_safety_eval.runner.evaluator import Evaluator


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(prog="coding-safety-eval")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    run = subparsers.add_parser("run")
    run.add_argument("--task", required=True)
    run.add_argument("--agent", choices=["manual-safe", "manual-unsafe", "openrouter"], required=True)
    run.add_argument("--model")
    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("results", type=Path)
    args = parser.parse_args()
    root = project_root()
    tasks = discover_tasks(root / "tasks")
    if args.command == "list":
        for task in tasks.values():
            print(f"{task.id}\t{task.category}\t{task.title}")
        return
    if args.command == "summarize":
        rows = [json.loads(p.read_text()) for p in args.results.rglob("*.json")]
        print(json.dumps(aggregate(rows), indent=2))
        return
    agent = OpenRouterAgent(args.model) if args.agent == "openrouter" else ManualPatchAgent(args.agent.removeprefix("manual-"))
    evaluator = Evaluator(root, root / "results" / "runs", root / "trajectories" / "runs")
    result = evaluator.evaluate(tasks[args.task], agent)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
