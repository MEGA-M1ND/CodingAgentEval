# Interview notes

**Why build it?** Coding agents increasingly make repository-level changes, and functional success alone does not establish safety.

**What failure does it measure?** False success: the agent appears successful from visible signals but violates hidden security or evaluator-integrity requirements.

**Why hidden tests?** They distinguish generalization from optimizing directly against known evaluator behavior.

**Why integrity separately?** Editing tests can optimize the metric without solving the task.

**Why deterministic graders?** Invariants such as unauthorized access and SQL injection are more repeatable and interpretable as executable tests than subjective model judgments.

**V1:** larger repository tasks, restricted tool-loop agents, Semgrep/Bandit/CodeQL integration, multiple agents and repeated stochastic runs, adversarial repository content, dependency attacks, calibrated LLM judging, and confidence intervals.
