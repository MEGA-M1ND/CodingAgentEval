# Threat model

The system under evaluation is a coding agent modifying a task workspace. Studied threats include vulnerable code, weakened constraints, evaluator/test manipulation, and premature completion claims.

V0 does not fully address malicious generated binaries, kernel or container escapes, hostile dependency installation, arbitrary internet exfiltration, sophisticated DNS rebinding, or secrets present in the host environment. It uses copied workspaces, bounded test subprocesses, a small environment allowlist, and no public-network-dependent fixtures. Use a hardened sandbox before evaluating untrusted agents or code in production-like settings.
