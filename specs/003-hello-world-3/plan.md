# Implementation Plan: Hello World 3 Executable

**Branch**: `003-hello-world-3` | **Date**: 2026-08-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-hello-world-3/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Provide a single, dependency-free Python script that can be invoked directly and prints the literal text `hello world 3` to standard output, then exits successfully. The script is a standalone smoke-test/tooling utility (not a `monai` library feature), so it is placed at the repository root under a new `scripts/` directory, outside the installable `monai` package, with a corresponding `pytest` test under `tests/` that exercises it as a black-box CLI.

## Technical Context

**Language/Version**: Python (project-supported CPython versions, matching `setup.cfg` `python_requires = >= 3.10`)

**Primary Dependencies**: None inside the script itself (a bare `print()` call suffices). The test module uses `sys` (for `sys.executable`) and `subprocess` from the standard library only — no third-party or optional imports anywhere in this feature.

**Storage**: N/A (stateless, no persisted data)

**Testing**: `pytest`, invoking the script as a subprocess (`subprocess.run([sys.executable, path], ...)`) from a test module under `tests/`

**Target Platform**: Cross-platform — any OS/Python environment already supported by the MONAI project (Linux/macOS/Windows CI matrix)

**Project Type**: Single standalone CLI script (repo-root tooling utility), not part of the `monai` library package

**Performance Goals**: Prints output and exits within 1 second of invocation (per SC-001); no throughput/latency targets beyond that

**Constraints**: No CLI arguments, configuration, network, filesystem, or optional dependencies required; must be deterministic and stateless across repeated/concurrent invocations (FR-005, FR-006)

**Scale/Scope**: Minimal — one script file plus one test file; no data model, no public API surface

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Medical Imaging Focus**: This is a generic "hello world" smoke-test utility with no medical-imaging content, so it MUST NOT be added inside the `monai` package (which is scoped to medical-imaging-specific or domain-enabling code). **Resolution**: the script is placed at the repository root under `scripts/`, entirely outside `monai/`, alongside other non-domain repo tooling (e.g. `runtests.sh`, `versioneer.py`). It ships no public library API and is not imported by `monai`. Gate: **PASS** (with placement constraint enforced; tracked below for transparency, not a true violation since it never enters the package scope).
- **II. Compositional & Portable APIs**: N/A — no public API is introduced; nothing to compose or import lazily (no optional dependencies used at all). Gate: **PASS**.
- **III. Test Strength (NON-NEGOTIABLE)**: A test module `tests/test_hello_world_3.py` will exercise normal invocation, repeated/deterministic invocation, and the "ignore extra arguments" edge case, asserting exact stdout and success exit code. Gate: **PASS** (planned).
- **IV. API Lifecycle & Compatibility**: N/A — no public API, no deprecations, nothing to break. Gate: **PASS**.
- **V. Quality, Library Conventions & Documentation**: The script MUST pass black/isort/ruff, carry the Apache-2.0 MONAI Consortium license header, use a Google-style docstring, and use American English spelling, consistent with other source files in this repo even though it lives outside `monai/`. Gate: **PASS** (planned).

No violations requiring justification beyond the placement note above; see Complexity Tracking (empty — no deviations to justify).

## Project Structure

### Documentation (this feature)

```text
specs/003-hello-world-3/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
scripts/
└── hello_world_3.py     # Standalone executable script (feature entry point); has
                          # a main() function and an `if __name__ == "__main__"` guard

tests/
└── test_hello_world_3.py  # pytest module; invokes the script as a subprocess and
                            # asserts stdout text, exit code, determinism, and that
                            # extra CLI arguments are ignored
```

**Structure Decision**: Single standalone script under a new repository-root
`scripts/` directory (`scripts/hello_world_3.py`), kept outside the installable
`monai/` package because this is a generic smoke-test utility, not a
medical-imaging library feature (Constitution Principle I). Its test lives under
the existing `tests/` directory as `tests/test_hello_world_3.py`, following the
project's `test_[module].py` naming convention (Constitution Principle III). No
other directories are introduced.

## Complexity Tracking

> No Constitution Check violations require justification. The feature is scoped
> and placed (`scripts/`, outside `monai/`) specifically to avoid any conflict
> with Principle I (Medical Imaging Focus); this table is intentionally empty.
