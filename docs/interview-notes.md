# Interview notes

**Why build it?** Coding agents increasingly make repository-level changes, and functional success alone does not establish safety.

**What failure does it measure?** False success: the agent appears successful from visible signals but violates hidden security or evaluator-integrity requirements.

**Why hidden tests?** They distinguish generalization from optimizing directly against known evaluator behavior.

**Why integrity separately?** Editing tests can optimize the metric without solving the task.

**Why deterministic graders?** Invariants such as unauthorized access and SQL injection are more repeatable and interpretable as executable tests than subjective model judgments.

**V1:** larger repository tasks, restricted tool-loop agents, Semgrep/Bandit/CodeQL integration, multiple agents and repeated stochastic runs, adversarial repository content, dependency attacks, calibrated LLM judging, and confidence intervals.

Before running real models, I validated the evaluator using paired known-safe and known-unsafe implementations. Then I added a bounded coding-agent loop where models can inspect repository files, edit code, and run visible tests. Hidden security and integrity graders execute only after the agent declares completion. That distinguishes apparent success from safe success. Arbitrary shell access is excluded so the harness does not become unrestricted hostile-code execution.

One of the first real-agent smoke tests failed before meaningful coding behavior occurred. The model used a semantically reasonable but schema-incompatible field name (`filename` instead of `path`). Rather than running the planned benchmark and misclassifying those failures as model safety failures, I stopped the experiment, preserved the preregistration, and separated protocol compatibility from coding-agent performance. I then introduced and independently validated a model-independent canonicalization layer before defining a new experiment revision.
