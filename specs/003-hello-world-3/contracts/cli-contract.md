# CLI Contract: `scripts/hello_world_3.py`

**Feature**: [spec.md](../spec.md) | **Plan**: [plan.md](../plan.md)

This document defines the externally observable contract of the executable,
independent of implementation details.

## Invocation

```text
python scripts/hello_world_3.py [any arguments...]
```

- **Arguments**: None are required. Any arguments passed MUST be ignored
  (FR-005) — the contract below still holds regardless of what is passed.
- **Standard input**: Not read. The script MUST NOT block waiting for input
  (FR-004).
- **Environment/configuration**: None required.

## Output Contract

- **Standard output**: Exactly the text `hello world 3`, optionally followed by
  a single trailing newline. No leading/trailing decoration, no extra lines,
  no logging noise (FR-002, FR-007).
- **Standard error**: No output expected during normal operation.
- **Exit code**: `0` (success) on every normal invocation (FR-003, SC-004).

## Behavioral Guarantees

- **Determinism**: Identical output and exit code on every invocation, with no
  shared state across invocations (FR-006).
- **Concurrency-safe**: Multiple simultaneous invocations MUST NOT interfere
  with one another; each independently produces the same output (Edge Cases).
- **Redirection-safe**: Output MUST be correctly written whether standard
  output is a terminal, a redirected file, or a pipe (Edge Cases).
- **Latency**: Output MUST appear and the process MUST exit within 1 second of
  invocation under normal conditions (SC-001).

## Example

```text
$ python scripts/hello_world_3.py
hello world 3
$ echo $?
0
```
