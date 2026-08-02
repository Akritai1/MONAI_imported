---

description: "Task list template for feature implementation"
---

# Tasks: Hello World 3 Executable

**Input**: Design documents from `/specs/003-hello-world-3/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-contract.md, quickstart.md

**Tests**: Included — Constitution Principle III (Test Strength, NON-NEGOTIABLE) requires meaningful tests for all new functionality, and plan.md's Project Structure explicitly designates `tests/test_hello_world_3.py` as a deliverable.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. All three user stories exercise the same single script (`scripts/hello_world_3.py`); its core implementation is therefore built once in the Foundational phase, and each user story phase adds/validates the tests specific to that story's scenarios.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Per `plan.md` Project Structure: single standalone script at repository root, outside the `monai` package.

- `scripts/hello_world_3.py` — the executable
- `tests/test_hello_world_3.py` — its pytest test module

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create the `scripts/` directory at the repository root (new location per `plan.md` Project Structure; does not yet exist in the repo)

**Checkpoint**: `scripts/` directory exists and is ready to hold the executable.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core artifact that MUST exist before ANY user story can be tested, since all three user stories exercise the same executable

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Implement `scripts/hello_world_3.py`: add the Apache-2.0 MONAI Consortium license header (matching header conventions used in `monai/` source files), a Google-style module docstring, a `main()` function that prints exactly `hello world 3` to standard output, and an `if __name__ == "__main__": main()` guard. `main()` MUST ignore any `sys.argv` arguments, require no input/configuration, and return/exit successfully (status `0`). Satisfies FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007 and the contract in `specs/003-hello-world-3/contracts/cli-contract.md`.
- [X] T003 [P] Run `black`, `isort`, and `ruff check` against `scripts/hello_world_3.py` (per `pyproject.toml` project-wide configuration) and fix any violations, satisfying Constitution Principle V (depends on T002)

**Checkpoint**: `python scripts/hello_world_3.py` manually prints `hello world 3` and exits `0`; foundation ready for all user stories.

---

## Phase 3: User Story 1 - Run the executable and see the greeting (Priority: P1) 🎯 MVP

**Goal**: A user invokes the executable directly and sees the exact text `hello world 3` printed, with a successful exit status.

**Independent Test**: Run `python scripts/hello_world_3.py` from a terminal with no arguments; confirm `hello world 3` is printed to standard output and the process exits with status `0`.

### Tests for User Story 1

> **NOTE: Write these tests FIRST against the T002 implementation; they validate, not duplicate, the Foundational work**

- [X] T004 [P] [US1] Add `test_prints_hello_world_3_and_exits_success` to `tests/test_hello_world_3.py`: invoke `scripts/hello_world_3.py` via `subprocess.run([sys.executable, ...])` with no arguments, assert `stdout` equals `hello world 3` (allowing at most one trailing newline) and `returncode == 0` (Spec Acceptance Scenarios 1–2; `contracts/cli-contract.md`)
- [X] T005 [P] [US1] Add `test_requires_no_input_or_configuration` to `tests/test_hello_world_3.py`: invoke the script with `stdin` closed/empty and no special environment variables set, assert it completes within 1 second without hanging or raising an error (FR-004; SC-001)

### Implementation for User Story 1

- [X] T006 [US1] Run `pytest tests/test_hello_world_3.py -k "prints_hello_world_3_and_exits_success or requires_no_input_or_configuration" -v`, confirm both tests pass against `scripts/hello_world_3.py`, and adjust the script if any discrepancy is found (depends on T002, T004, T005)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently — this is the MVP.

---

## Phase 4: User Story 2 - Call the executable repeatedly or from scripts/automation (Priority: P2)

**Goal**: The executable behaves deterministically and statelessly when called multiple times, including from non-interactive scripts/automation and concurrently.

**Independent Test**: Invoke the executable multiple times in sequence (including from a non-interactive script with no attached terminal) and verify identical output and exit status on every run.

### Tests for User Story 2

- [X] T007 [P] [US2] Add `test_repeated_invocations_are_deterministic` to `tests/test_hello_world_3.py`: invoke the script at least 100 consecutive times in a loop, assert identical `stdout` and `returncode == 0` on every single run with no leftover state affecting later runs (FR-006; SC-002; Acceptance Scenario 1)
- [X] T008 [P] [US2] Add `test_runs_noninteractively_with_redirected_output` to `tests/test_hello_world_3.py`: invoke the script with `stdout` captured/piped and `stdin` redirected from an empty source (simulating a non-interactive CI/script call), assert the correct output is still produced without requiring user input (Acceptance Scenario 2; Edge Cases — output redirection)
- [X] T009 [P] [US2] Add `test_extra_arguments_are_ignored` to `tests/test_hello_world_3.py`: invoke the script with unexpected extra CLI arguments, assert output and exit code are unchanged from the no-argument case (FR-005; Edge Cases)
- [X] T010 [P] [US2] Add `test_concurrent_invocations_do_not_interfere` to `tests/test_hello_world_3.py`: launch several instances of the script at approximately the same time (e.g. via `concurrent.futures.ThreadPoolExecutor` each running a `subprocess.run`, or multiple `subprocess.Popen` started in a loop and then waited on), assert every instance independently produces `stdout == "hello world 3"` and `returncode == 0` (FR-006; Edge Cases — concurrent invocation)

### Implementation for User Story 2

- [X] T011 [US2] Run the four User Story 2 tests above (`pytest tests/test_hello_world_3.py -k "deterministic or noninteractive or extra_arguments or concurrent" -v`), confirm they pass unmodified against `scripts/hello_world_3.py`, and fix the script if any test reveals hidden state or argument-handling issues (depends on T002, T007, T008, T009, T010)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Discover how to call the executable (Priority: P3)

**Goal**: A new user can locate and run the executable using only its name/path, with no additional setup, configuration, or documentation beyond knowing where it is.

**Independent Test**: A user with no prior knowledge locates `scripts/hello_world_3.py` and successfully runs it using only its path, without needing extra setup.

### Tests for User Story 3

- [X] T012 [P] [US3] Add `test_callable_directly_by_path_with_no_setup` to `tests/test_hello_world_3.py`: invoke `scripts/hello_world_3.py` using only its relative path from the repository root, in a subprocess with a minimal/clean environment (no extra env vars or config files), and assert it runs immediately and produces the expected output (Acceptance Scenario 1; SC-003)

### Implementation for User Story 3

- [X] T013 [US3] Run the User Story 3 test above, confirm it passes, and cross-check it against the "Discoverability" step in `specs/003-hello-world-3/quickstart.md`, updating that doc if any manual step was found to be missing (depends on T002, T012)

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all user stories

- [X] T014 [P] Run the full test module `pytest tests/test_hello_world_3.py -v` and confirm all tests from User Stories 1–3 pass together, satisfying SC-004 (100% success exit status across all invocations)
- [X] T015 [P] Manually execute the full `specs/003-hello-world-3/quickstart.md` validation guide end-to-end (basic invocation, repeated/piped invocation, extra-argument invocation) and confirm actual behavior matches every documented expectation
- [X] T016 Review `scripts/hello_world_3.py` and `tests/test_hello_world_3.py` against Constitution Principle V (license header, Google-style docstrings, American English spelling, black/isort/ruff clean) and Principle III (`test_[module].py` naming convention), fixing any gaps found (depends on T002–T013)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories (the shared script must exist before any story's tests can run)
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed), since each only adds tests against the already-implemented, unmodified `scripts/hello_world_3.py`
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — no dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) — independently testable; does not require US1's tests to exist
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) — independently testable; does not require US1/US2's tests to exist

### Within Each User Story

- Tests are written against the already-completed Foundational implementation (T002)
- The "Implementation" task within each story phase is a validation/fix-forward step, not new feature code, since T002 already implements the full contract
- Story complete before moving to next priority (if working sequentially)

### Parallel Opportunities

- T003 (lint/format) can run in parallel with nothing else in Phase 2 (it depends on T002 completing first, so it is marked `[P]` only relative to other same-phase work, not to T002)
- Once Foundational (Phase 2) completes, all three user story test-writing tasks (T004+T005, T007+T008+T009+T010, T012) can proceed in parallel, since each appends independent test functions to the same file but touches no shared state
- T014 and T015 in Polish can run in parallel with each other

---

## Parallel Example: User Story 1

```bash
# Launch both User Story 1 tests together (after T002/T003 complete):
Task: "Add test_prints_hello_world_3_and_exits_success to tests/test_hello_world_3.py"
Task: "Add test_requires_no_input_or_configuration to tests/test_hello_world_3.py"
```

## Parallel Example: Across User Stories (post-Foundational)

```bash
# Once Foundational (T002, T003) is done, all story test-writing tasks can proceed in parallel:
Task: "[US1] Add test_prints_hello_world_3_and_exits_success + test_requires_no_input_or_configuration"
Task: "[US2] Add test_repeated_invocations_are_deterministic + test_runs_noninteractively_with_redirected_output + test_extra_arguments_are_ignored + test_concurrent_invocations_do_not_interfere"
Task: "[US3] Add test_callable_directly_by_path_with_no_setup"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002-T003) — this alone already produces a working, callable executable
3. Complete Phase 3: User Story 1 (T004-T006)
4. **STOP and VALIDATE**: Run `python scripts/hello_world_3.py` and the US1 tests independently
5. This is a fully demoable MVP satisfying the feature's primary value

### Incremental Delivery

1. Complete Setup + Foundational → executable exists and works
2. Add User Story 1 tests → validate independently → MVP demo-ready
3. Add User Story 2 tests → validate independently → confirms automation/repeatability/concurrency
4. Add User Story 3 tests → validate independently → confirms discoverability
5. Each story only adds test coverage; no story requires re-implementing the script

### Parallel Team Strategy

With multiple contributors:

1. One contributor completes Setup + Foundational (T001-T003) first, since it blocks everything else
2. Once Foundational is done:
   - Contributor A: User Story 1 tests (T004-T006)
   - Contributor B: User Story 2 tests (T007-T011)
   - Contributor C: User Story 3 tests (T012-T013)
3. All converge on Phase 6 Polish once their story's checkpoint passes

---

## Notes

- [P] tasks = different test functions or independent checks, safe to work on concurrently
- [Story] label maps task to specific user story for traceability
- All tests live in the single file `tests/test_hello_world_3.py`, so when working in parallel, contributors should add distinct test functions to avoid merge conflicts, then merge and re-run T014 together
- Verify each new test fails only if the underlying behavior is actually broken — since T002 is complete before any test task begins, tests are expected to pass immediately; treat any failure as a Foundational bug to fix, not as expected TDD "red" state
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
