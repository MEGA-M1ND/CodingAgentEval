# Methodology

The research question is: can a coding agent complete an engineering task while preserving functionality, security, and evaluation integrity? One experimental unit is one agent × one task × one configuration. Each result separately records functionality, security, integrity, and efficiency.

V0 uses deterministic executable graders whenever a property can be objectively checked. This improves repeatability, calibration, interpretability, and cost. LLM-as-judge is intentionally excluded because semantic grading is not needed for these invariants and would make benchmark changes harder to diagnose.

The workspace is a temporary copy of a task fixture. Hidden tests remain in the benchmark source and import the candidate workspace only while grading. Protected visible test files are hashed before execution and compared afterward. V0 therefore simulates a protected evaluator boundary; it does not claim hardened isolation from malicious code.
