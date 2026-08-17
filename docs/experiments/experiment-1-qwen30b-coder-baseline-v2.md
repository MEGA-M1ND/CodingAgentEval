# Experiment 1 — Qwen 30B Coder Safety Baseline (Pre-registered)

## Research question

Does visible functional success overestimate safe completion for the fixed
Qwen coding-agent model on security-sensitive software-engineering tasks?

## Hypotheses

- **H1:** safe success rate will be lower than visible functional success rate
  (`safe_success_rate < functional_success_rate`).
- **H2:** at least one run will exhibit `FALSE_SUCCESS`.
- **H3:** security failures will account for more failed-safe outcomes than
  evaluation-integrity violations.

These are hypotheses, not assumptions; negative results will be reported
unchanged.

## Experimental unit and design

One model × task × repetition. The planned experiment is one fixed model, six
tasks, and three independent repetitions: **18 planned model runs**. The smoke
run is excluded from Experiment 1 statistics.

Tasks: `auth-bypass-001`, `sql-injection-001`, `command-injection-001`,
`path-traversal-001`, `ssrf-001`, and `test-tampering-001`.

## Frozen configuration

| Field | Value |
| --- | --- |
| Experiment ID | `exp1-qwen30b-coder-baseline-v2` |
| Model | `qwen/qwen3-coder-30b-a3b-instruct` |
| Temperature | `0` |
| Max steps | `20` |
| System prompt | `neutral-v1` |
| Grader version | `v1` |
| Git commit before execution | `7a27887e860d0a6470f2c5e63bfa4fd438b6330d` |
| Manifest SHA-256 | `C518B0820F4D6B594D83B44B58760426B58E3778226BEC2967A0202E8B2275E4` |

The model receives only the user-facing task, visible workspace, visible test
output, and bounded tools. It does not receive hidden tests, hidden properties,
reference solutions, task metadata, or grader implementation.

## Metrics

Primary: safe success rate. Secondary: functional success, security success,
false-success, integrity-violation, and execution-error rates; mean/median
steps and latency; input/output/total tokens; and cost where supplied by
OpenRouter. Results are reported globally and per task.

The visible-to-safe gap is `functional_success_rate - safe_success_rate`.
Infrastructure-level `EXECUTION_ERROR` is reported separately and is never
counted as a model safety failure.

## Stopping rules

Run all 18 planned runs only if the pre-experiment smoke validates the required
read, write, visible-test, and finish sequence. Stop if credentials are
unavailable, a benchmark defect invalidates measurement, or infrastructure-level
execution errors exceed 20% of planned runs. The harness's bounded provider
retry behavior is the only retry behavior used; outcome failures are not rerun
for selection.

## Analysis plan

Raw results, trajectories, and final diffs will be preserved. Non-safe outcomes
will be categorized using observable behavior only: tool actions, writes,
visible tests, finish event, patch, and grader result. Up to three false-success
cases and one safe-success case will be described without exposing hidden test
source.

This is a small synthetic benchmark and will be interpreted as evidence only
within these six tasks, this model configuration, and three repetitions.
