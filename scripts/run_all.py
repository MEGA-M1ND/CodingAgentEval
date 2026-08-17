"""Run a deterministic manifest using manual safe/unsafe fixtures."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from coding_safety_eval.agents.manual_patch_agent import ManualPatchAgent
from coding_safety_eval.models.task import discover_tasks
from coding_safety_eval.runner.evaluator import Evaluator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--agent", choices=["manual-safe", "manual-unsafe"], default=None)
    args = parser.parse_args()
    manifest = yaml.safe_load(args.manifest.read_text())
    agent_name = args.agent or manifest.get("agent", "manual-safe")
    agent = ManualPatchAgent(agent_name.removeprefix("manual-"))
    label = "safe" if agent_name == "manual-safe" else "unsafe"
    evaluator = Evaluator(ROOT, ROOT / "results" / "baseline-validation" / label, ROOT / "trajectories" / "baseline-validation" / label)
    tasks = discover_tasks(ROOT / "tasks")
    for task_id in manifest["tasks"]:
        result = evaluator.evaluate(tasks[task_id], agent)
        print(f"{task_id}: {result.classification}")


if __name__ == "__main__":
    main()
