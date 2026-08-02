<!--
Sync Impact Report
- Version change: (none) → 1.0.0
- Modified principles: N/A (initial ratification)
- Added sections:
  - Core Principles: I. No Deprecated API Usage, II. No Anti-Patterns,
    III. No Missing or Weak Tests (NON-NEGOTIABLE)
  - Quality Gates & Tooling
  - Development Workflow & Review Process
  - Governance
- Removed sections: N/A (initial ratification)
- Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending manual review (verify Constitution
    Check gates reference deprecated-API, anti-pattern, and test-coverage checks)
  - .specify/templates/spec-template.md ✅ no changes required (principle-agnostic)
  - .specify/templates/tasks-template.md ⚠ pending manual review (ensure task
    generation includes explicit test-writing and deprecation-check tasks)
  - .specify/templates/checklist-template.md ✅ no changes required (generic)
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Original ratification date is unknown; set to the date
    this constitution was first adopted (2026-08-02) pending confirmation from
    project maintainers.
-->

# MONAI Constitution

## Core Principles

### I. No Deprecated API Usage (NON-NEGOTIABLE)

New and modified code MUST NOT introduce new call sites of any API, argument, or module
already marked deprecated (via `monai.utils.deprecated`, `monai.utils.deprecated_arg`,
docstring `.. deprecated::` notes, or an equivalent explicit deprecation warning).
Contributions MUST migrate to the documented replacement API instead of extending usage
of the old one. Introducing a *new* deprecation MUST follow MONAI's established backward
compatibility process end to end:

1. The deprecated API MUST continue to function and MUST emit a `DeprecationWarning`
   (or `FutureWarning`, per `monai.utils.deprecated`) that names the removal target
   version and the recommended replacement.
2. The replacement API MUST provide equivalent functionality so users can migrate
   without loss of capability.
3. Unit tests MUST be extended to exercise both the deprecated path (asserting the
   warning is raised and legacy behavior is preserved) and the new path, until the
   deprecated API is removed.
4. Removal MUST NOT happen before the announced version and MUST be re-reviewed at
   each release to confirm the migration window has elapsed before deletion.

Rationale: MONAI is consumed by clinical and research pipelines where silent breakage or
unbounded API churn erodes trust and reproducibility. A single, auditable deprecation path
keeps the library upgradeable without surprising downstream users.

### II. No Anti-Patterns

Code MUST be free of known anti-patterns before it can be merged. This includes, at minimum:

- Mutable default arguments (`def f(x=[])`), bare `except:` clauses, and broad
  `except Exception` blocks that silently swallow errors.
- Wildcard imports (`from module import *`) outside of package `__init__.py` re-exports
  that are intentional and use `__all__`.
- Copy-pasted/duplicated logic where a shared utility or existing MONAI abstraction
  (e.g. `Transform`, `MapTransform`, existing losses/metrics/networks) already exists.
- Public functions, classes, or methods without docstrings, or with parameters,
  return values, or raised exceptions undocumented in Google-style docstrings.
- Oversized, multi-responsibility functions/classes ("God functions/classes") where a
  focused decomposition is practical.
- Ignoring or suppressing linter/type-checker findings (`# noqa`, `# type: ignore`, or
  disabling a `ruff`/`mypy` rule) without an inline comment justifying why the
  suppression is necessary and safe.
- New public/exported symbols that are not added to the module's `__all__` and the
  package's `__init__.py`, per MONAI's exporting convention.

Automated tooling (`black`, `isort`, `ruff`, DeepSource) enforces a baseline subset of
this principle, but tooling passing is necessary, not sufficient — reviewers MUST also
manually screen for the anti-patterns above that static analysis cannot fully catch.

Rationale: Anti-patterns compound maintenance cost and defect risk across a
large, community-contributed codebase. Naming the concrete anti-patterns to reject
makes code review objective and consistent instead of relying on reviewer intuition.

### III. No Missing or Weak Tests (NON-NEGOTIABLE)

*If it's not tested, it's broken.* Every new feature, bug fix, or behavioral change MUST
ship with automated tests in `tests/` following the `test_[module_name].py` /
`test_[module_name]_dist.py` / `test_integration_[workflow_name].py` conventions. A test
suite is considered missing or weak — and therefore blocking — if any of the following apply:

- A new public function, class, transform, network, loss, or metric has zero
  corresponding test cases.
- A bug fix has no regression test that fails against the pre-fix code and passes
  against the fix.
- Tests only exercise the "happy path" and omit documented edge cases (empty inputs,
  boundary shapes/dtypes, GPU/CPU and distributed variants where applicable, invalid
  arguments expected to raise).
- Tests assert on trivial or tautological conditions (e.g. asserting a mock's return
  value equals itself) instead of verifying real behavior against expected outputs.
- Numerical assertions use bare equality on floating-point results instead of the
  appropriate tolerance-based assertion.
- Code coverage for changed lines regresses without an explicit, reviewer-accepted
  justification (e.g. defensive code that is deliberately unreachable).

Every pull request MUST pass `./runtests.sh --codeformat` (or `--ruff` for a fast
check) and the relevant unit test suite (`./runtests.sh --quick --unittests` for
additive changes, or `./runtests.sh -f -u --net --coverage` for changes touching
existing behavior) before it can be merged.

Rationale: MONAI's test suite is the primary guarantee of correctness for
safety-relevant medical imaging workflows. Treating test gaps as blocking — not
advisory — prevents regressions from reaching downstream clinical and research users.

## Quality Gates & Tooling

The following automated gates back the Core Principles and MUST remain green (or have
an explicit, documented maintainer override) before merge:

- **Formatting & linting**: `black`, `isort`, and `ruff` via `./runtests.sh --codeformat`
  / `--autofix`.
- **Static analysis**: DeepSource `python` and `test-coverage` analyzers as configured
  in `.deepsource.toml`.
- **Automated review**: CodeRabbit path-specific review rules (`.coderabbit.yaml`),
  which explicitly check for unit test coverage of new/modified definitions and
  documentation completeness.
- **CI test matrices**: the premerge/postmerge GitHub Actions workflows, including
  minimal-dependency runs (`tests/min_tests.py`) and coverage reporting to CodeCov.

A PR MAY NOT be merged solely on the basis of green CI if a human reviewer has
identified an unaddressed deprecated-API usage, anti-pattern, or test gap under
Principles I–III; automated gates are a floor, not a substitute for review judgment.

## Development Workflow & Review Process

- Reviewers MUST explicitly check each pull request against Principles I (no new
  deprecated-API usage, or a complete deprecation plan if one is intentionally
  introduced), II (no anti-patterns), and III (tests present and meaningful) before
  approving.
- When a PR intentionally introduces a new deprecation, the PR description MUST state
  the target removal version and the replacement API, consistent with
  `CONTRIBUTING.md`'s backward-compatibility process.
- Complexity, duplication, or suppressed lint/type warnings MUST be justified inline in
  code comments or in the PR description; unjustified instances are grounds for
  requesting changes.
- Before each release, deprecated APIs approaching their announced removal version MUST
  be reviewed and removed along with their compatibility tests, per Principle I.

## Governance

This constitution codifies MONAI's minimum, non-negotiable code-quality bar and takes
precedence over informal conventions when they conflict; it supplements, and does not
replace, the fuller guidance in `CONTRIBUTING.md`.

- **Amendments**: Proposed via pull request modifying this file, including a completed
  Sync Impact Report (as an HTML comment at the top of the file) describing the version
  bump rationale and any dependent template updates. Amendments require review and
  approval from a MONAI maintainer with governance authority before merge.
- **Versioning policy**: This constitution follows semantic versioning:
  - **MAJOR** — backward-incompatible governance changes, or removal/redefinition of an
    existing principle.
  - **MINOR** — a new principle or materially expanded guidance is added.
  - **PATCH** — clarifications, wording, or non-semantic refinements.
- **Compliance review**: All pull requests and code reviews MUST verify compliance with
  the Core Principles above. Reviewers who observe a violation MUST block the merge
  until it is resolved or an explicit, documented exception is granted by a maintainer.
- Use `CONTRIBUTING.md` for detailed day-to-day development, testing, and style
  guidance that operationalizes the principles defined here.

**Version**: 1.0.0 | **Ratified**: 2026-08-02 | **Last Amended**: 2026-08-02
