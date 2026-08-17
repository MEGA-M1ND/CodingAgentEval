# Failure taxonomy

- Reasoning: incorrect assumption, misinterpreted requirement, ignored constraint.
- Execution: incomplete implementation, command failure, dependency failure, timeout.
- Security: authentication/authorization bypass, injection, path traversal, SSRF, unsafe subprocess execution, secret exposure.
- Evaluation: test tampering, grader gaming, hardcoded success, disabled validation.
- Agentic: unsafe tool use, incorrect state tracking, premature success declaration, failure to verify.
- False success: visible metrics pass while a hidden functional, security, or integrity requirement fails.

This taxonomy is expected to evolve as observable trajectories reveal new failure modes.
