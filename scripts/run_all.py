"""Execute one manifest into a unique, contamination-free artifact directory."""

from __future__ import annotations

import argparse
import os
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from coding_safety_eval.agents.manual_patch_agent import ManualPatchAgent
from coding_safety_eval.agents.openrouter_agent import OpenRouterAgent
from coding_safety_eval.models.task import discover_tasks
from coding_safety_eval.runner.evaluator import Evaluator
from coding_safety_eval.utils.environment import load_dotenv


def _expand(value: str | None) -> str | None:
    if value and value.startswith("${") and value.endswith("}"):
        return os.getenv(value[2:-1])
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--agent", choices=["manual-safe", "manual-unsafe", "openrouter"])
    parser.add_argument("--execution-id")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    manifest = yaml.safe_load(args.manifest.read_text())
    agent_name = args.agent or manifest["agent"]
    model = _expand(manifest.get("model"))
    if agent_name.startswith("manual-"):
        agent = ManualPatchAgent(agent_name.removeprefix("manual-"))
        label = agent_name
    else:
        agent = OpenRouterAgent(model, max_steps=int(manifest.get("max_steps", 20)), temperature=float(manifest.get("temperature", 0)), system_prompt_version=str(manifest.get("system_prompt_version", "neutral-v2")))
        label = (model or "unconfigured").replace("/", "-")
    execution_id = args.execution_id or f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
    experiment_id = manifest["experiment_id"]
    results_root = ROOT / "results" / experiment_id / execution_id / label
    trajectories_root = ROOT / "trajectories" / experiment_id / execution_id / label
    config = {key: manifest[key] for key in ("grader_version", "temperature", "max_steps", "system_prompt_version") if key in manifest}
    evaluator = Evaluator(ROOT, results_root, trajectories_root, experiment_id=experiment_id, execution_id=execution_id, configuration=config)
    tasks = discover_tasks(ROOT / "tasks")
    for task_id in manifest["tasks"]:
        result = evaluator.evaluate(tasks[task_id], agent)
        print(f"{task_id}: {result.classification}")
    print(f"\nExperiment complete.\n\nexperiment_id: {experiment_id}\nexecution_id: {execution_id}\n\nResults:\n{results_root}")


if __name__ == "__main__":
    main()
