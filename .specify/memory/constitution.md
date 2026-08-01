<!--
Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- Modified principles:
  - III. Test Coverage (NON-NEGOTIABLE) → III. Test Strength (NON-NEGOTIABLE)
  - IV. API Stability & Compatibility → IV. API Lifecycle & Compatibility
  - V. Quality, Typing & Documentation → V. Quality, Library Conventions & Documentation
- Added sections: none
- Removed sections: none
- Follow-up TODOs: none
-->

# MONAI Constitution

## Core Principles

### I. Medical Imaging Focus
MONAI MUST remain a PyTorch-based framework for deep learning in healthcare
imaging. Features MUST be medical-application specific or clearly justified as
domain-enabling infrastructure. General-purpose deep learning or scientific
computing that belongs in PyTorch or NumPy MUST NOT be added here; contributors
MUST redirect such work upstream or keep it out of core.

Rationale: Scope discipline preserves a common foundation for academic,
industrial, and clinical imaging researchers without duplicating the PyTorch
ecosystem.

### II. Compositional & Portable APIs
Public APIs MUST be compositional, portable, and usable across expertise levels.
Modules MUST integrate into existing training and inference workflows without
forcing a single end-to-end application shape. Optional third-party capabilities
MUST be invoked lazily (for example via `optional_import`) so core installs with
minimal dependencies remain usable.

Rationale: Flexible pre-processing and portable APIs are core product goals;
eager optional imports break minimal environments and CI.

### III. Test Strength (NON-NEGOTIABLE)
All new functionality and bug fixes MUST ship with meaningful unit and/or
integration tests that exercise normal behavior, relevant edge cases, and
failure behavior. Untested or weakly tested behavior is treated as broken.
Tests MUST assert observable contracts rather than implementation details, and
MUST fail when the defect or feature implementation is removed. Tests MUST live
under `tests/` using established naming (`test_[module].py`,
`test_[module]_dist.py`, `test_integration_[workflow].py`). Large binary
fixtures MUST NOT enter the source tree; they MUST use the external test-data
mechanism. Features that need optional packages MUST skip or exclude cleanly in
minimal CI.

Rationale: Imaging transforms, networks, and distributed paths regress easily;
tests are the contract with users and CI.

### IV. API Lifecycle & Compatibility
Public API changes MUST prefer backward-compatible evolution. Breaking changes
MUST be deliberate, documented, and aligned with release policy. Dependency
support MUST follow project policy: currently supported Python versions; PyTorch
current plus recent minors; other dependencies aligned with SPEC0 where practical.
Major releases MAY pin or refresh dependency floors; `dev` tracks unreleased work.
New or changed public APIs MUST NOT introduce deprecated interfaces. Existing
deprecated APIs MUST be removed or migrated according to the documented release
policy; a deprecation exception requires explicit maintainer approval, a removal
version, and migration guidance.

Rationale: Research and clinical pipelines depend on stable, predictable upgrades.

### V. Quality, Library Conventions & Documentation
Contributions MUST pass project linting and formatting (black, isort, ruff) and
static typing expectations (mypy/pytype as configured). Public modules MUST
export intentionally via `__all__` and package `__init__` where appropriate.
User-facing behavior MUST be documented (Google-style docstrings; Sphinx docs as
needed). Source files MUST carry the Apache-2.0 MONAI Consortium license header.
American English spelling MUST be used in identifiers and docs. Implementations
MUST follow established MONAI library conventions in adjacent modules, including
API shape, error handling, imports, naming, and test layout. Anti-patterns
including duplicated logic, hidden global state, broad exception suppression,
eager optional imports, and unbounded abstractions MUST NOT be introduced.

Rationale: Consistent style, types, and docs keep a large community codebase
reviewable and usable.

## Technology Constraints

- Core runtime stack: Python (supported CPython versions), NumPy, and PyTorch.
- License: Apache License 2.0 for project contributions.
- Optional dependencies MUST be declared in the maintained dependency/docs
  surfaces (`setup.cfg` extras, `requirements-dev.txt`, docs requirements,
  `environment-dev.yml`, installation docs) when added.
- Distributed and GPU paths MUST remain first-class where the feature requires
  them; dedicated `*_dist` tests MUST cover those cases.
- Bundle and Model Zoo interoperability SHOULD prefer documented MONAI Bundle
  conventions when exposing reusable workflows.

## Contribution Workflow

- Prefer early draft pull requests for visibility of work in progress.
- Contributors MUST follow `CONTRIBUTING.md` for style, tests, docs, optional
  deps, and review expectations.
- All commits MUST be DCO signed-off (`Signed-off-by`); unsigned PRs MUST NOT
  merge.
- Reviewers MUST verify principle compliance, test strength, deprecated-API
  impact, library-convention adherence, and documentation before merge.
- Complexity and new abstractions MUST be justified against user need (YAGNI);
  speculative generality is not sufficient grounds to merge.

## Governance

This constitution supersedes informal practice when they conflict. Amendments
MUST update this file, bump `CONSTITUTION_VERSION` using semantic versioning
(MAJOR for incompatible principle removals/redefinitions, MINOR for new or
materially expanded principles/sections, PATCH for clarifications), and set
**Last Amended** to the amendment date. Ratification date remains the original
adoption date unless the project explicitly re-ratifies.

PRs and reviews MUST treat these principles as compliance checkpoints.
Runtime contribution detail remains in `CONTRIBUTING.md` and project docs;
this constitution defines non-negotiable product and engineering rules for
Spec Kit–driven and day-to-day development alike.

**Version**: 1.1.0 | **Ratified**: 2026-08-01 | **Last Amended**: 2026-08-01
