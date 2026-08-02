# Phase 0 Research: Hello World 3 Executable

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

All unknowns from the Technical Context have been resolved below; there are no
remaining `NEEDS CLARIFICATION` markers.

## Decision 1: Where to place the executable

**Decision**: Implement as a plain Python 3 script at `scripts/hello_world_3.py`
(repository root, outside the `monai` package), with a `main()` function guarded
by `if __name__ == "__main__": main()`.

**Rationale**: The MONAI Constitution's Principle I (Medical Imaging Focus)
restricts the `monai` package to medical-imaging-specific or clearly justified
domain-enabling infrastructure; a generic "hello world" smoke-test string has
neither property. Placing the script at the repository root under `scripts/`
keeps it fully outside the installable library surface (it is never imported by
`monai`, never appears in `find_packages()`, and ships no public API), which
satisfies the constitution without needing a justified exception. This mirrors
how other non-domain tooling already lives at the repo root (e.g. `runtests.sh`,
`versioneer.py`) rather than inside `monai/`.

**Alternatives considered**:
- Add it as `monai/apps/hello_world_3/__main__.py`, invokable via
  `python -m monai.apps.hello_world_3`, mirroring existing patterns like
  `monai/bundle/__main__.py` and `monai/apps/auto3dseg/__main__.py`. Rejected
  because it would ship non-domain functionality inside the public library
  package, directly conflicting with Principle I.
- Register a `console_scripts` entry point in `setup.cfg` (e.g.
  `hello-world-3 = ...:main`). Rejected as unnecessary complexity (YAGNI per the
  Contribution Workflow section) for a one-off smoke-test script; the spec does
  not require installation/distribution as a named system command, only that it
  be directly callable (e.g. `python scripts/hello_world_3.py`).

## Decision 2: Dependencies

**Decision**: Use only the Python standard library (a bare `print()` call); no
third-party or optional dependencies.

**Rationale**: FR-004 requires no configuration or setup, and Principle II
requires that optional third-party capabilities be invoked lazily so minimal
installs keep working. The simplest way to guarantee the script runs in every
environment, including minimal CI configurations, is to avoid dependencies
entirely.

**Alternatives considered**:
- Using `argparse` to build a CLI skeleton. Rejected: FR-005 requires that any
  extra arguments simply be ignored, and there is no other input to parse, so
  an argument-parsing framework would add complexity with no benefit (YAGNI).

## Decision 3: Testing approach

**Decision**: Add `tests/test_hello_world_3.py`, a `pytest` module that invokes
the script as a subprocess (`subprocess.run([sys.executable, script_path, ...],
capture_output=True, text=True)`) and asserts on `stdout`, `returncode`,
determinism across repeated calls, and that extra CLI arguments do not change
behavior.

**Rationale**: Constitution Principle III (Test Strength) requires meaningful
tests under `tests/` using the `test_[module].py` naming convention, asserting
observable contracts rather than implementation details. Testing via subprocess
validates the script exactly as an external user or automation would call it
(FR-001–FR-007), which is the actual observable contract for an "executable."

**Alternatives considered**:
- Importing the script's `main()` function directly and capturing output via
  pytest's `capsys` fixture. Rejected as the primary approach because it tests
  the Python function in-process rather than the "callable executable" contract
  itself (e.g., it would not catch issues with the `if __name__ == "__main__"`
  guard or process exit status), though nothing prevents also unit-testing
  `main()` directly if useful during implementation.

## Outstanding Unknowns

None. All Technical Context fields in `plan.md` are resolved.
