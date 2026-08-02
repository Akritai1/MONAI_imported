# Quickstart: Hello World 3 Executable

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Contract**: [contracts/cli-contract.md](./contracts/cli-contract.md)

## Prerequisites

- A Python interpreter matching the project's supported versions
  (`python_requires >= 3.10`, per `setup.cfg`). No third-party packages are
  required for this feature.
- Repository checked out locally, with the feature implemented at
  `scripts/hello_world_3.py`.

## Run It

From the repository root:

```bash
python scripts/hello_world_3.py
```

**Expected output**:

```text
hello world 3
```

**Expected exit code**: `0`

## Validate the Full Contract

1. **Basic invocation** (User Story 1): run the command above; confirm the
   exact text `hello world 3` is printed and the process exits successfully.

2. **Repeated / scripted invocation** (User Story 2): run it several times in a
   row, including piped/non-interactive contexts, and confirm identical output
   and success every time:

   ```bash
   for i in 1 2 3; do python scripts/hello_world_3.py; done
   python scripts/hello_world_3.py | cat
   ```

3. **Extra arguments are ignored** (Edge Case / FR-005):

   ```bash
   python scripts/hello_world_3.py --unexpected-flag some-value
   ```

   Expected: still prints `hello world 3` and exits `0`.

4. **Discoverability** (User Story 3): a new user can locate and run
   `scripts/hello_world_3.py` directly by name/path with no extra setup.

## Automated Tests

Run the corresponding test module with `pytest`:

```bash
pytest tests/test_hello_world_3.py -v
```

This exercises the same scenarios above (see
[contracts/cli-contract.md](./contracts/cli-contract.md) for the full contract
being validated) as part of CI.
