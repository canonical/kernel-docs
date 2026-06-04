---
name: documentation-verify
description: "Verifies documentation accuracy by cross-referencing claims, CLI commands, API signatures, and configuration against source code. Use when validating documentation correctness or checking code-docs consistency. Flags unsupported or outdated claims."
---

# Documentation Accuracy Verification

## Scope

Accuracy verification only: cross-reference documentation claims,
commands, API names, and configuration keys against repository evidence
in the same repository. Flag anything that cannot be verified.

In docs-only repositories, treat documentation tooling and artifacts
(for example, `conf.py`, `Makefile`, Sphinx configuration, redirects,
and examples) as the primary evidence source.

## Inputs

- Changed documentation files (from `git diff`).
  If `git diff` is unavailable or empty, use files explicitly provided
  for review; otherwise, treat all documentation files under the detected
  docs root as changed.
- Full repository artifacts relevant to documentation behavior.
- Test files and configuration schemas (when applicable).
- Documentation structure.

---

## Workflow

Follow this three-stage process to verify documentation accuracy:

### Stage 1: Discovery Scan

**Objective**: Identify documentation claims and form initial hypotheses.

1. Run `git diff` to list changed documentation files.
2. Categorize changes into claim types (behavior, CLI, API, config, examples, error messages, etc.).
3. Form initial hypotheses: Supported, Unsupported, Speculative, Ambiguous, or Outdated.

**For detailed categorization and hypothesis formation procedures**, see `references/verification_procedures.md` → Discovery Scan.

---

### Stage 2: Verification Pass

**Objective**: Verify every hypothesis with repository evidence.
Repository artifacts are the source of truth.

**CRITICAL**: Complete verification before reporting any claims.

1. Use **at least two search strategies** per claim (direct search, entrypoint tracing, test evidence, schema/validation search).
2. Apply claim-type-specific verification checklists (behavior, CLI, API, config, examples, errors, terminology).
3. Document evidence for each finding (file paths, line numbers, search commands).
4. Reclassify hypotheses based on verification results.
5. Apply false-positive prevention rules.
6. Cross-check documentation coverage.

**For comprehensive verification checklists and classification rules**, see `references/verification_procedures.md` → Verification Pass.

---

### Stage 3: Report Generation

**Objective**: Present verified findings with evidence and conservative recommendations.

1. Group findings by final classification (unsupported, outdated, incorrect, imprecise, speculative, inconclusive, no issues).
2. Format each finding using the standard template (doc claim, verification checklist, code evidence, assessment, recommended action).
3. Provide conservative change suggestions aligned with code reality.
4. Link to specific code artifacts (files, functions, structs, line numbers).
5. Integrate with other analysis findings (e.g., Diataxis compliance).

**For report formatting template and change suggestion guidelines**, see `references/report_format.md`.

---

## Constraints

- Complete the verification pass (Stage 2) before reporting any claims.
- Provide repository evidence for all documentation consistency claims.
- Repository artifacts are the source of truth: flag documentation that
  contradicts repository behavior, not vice versa.
- Do not claim documentation is "unsupported" without verification evidence
  (at least two search strategies with explicit search and no-match confirmation).
- Do not report false positives.
- Do not prefer "unsupported" when docs are vague or imprecise; use accurate classifications.
- Do not recommend changing implementation artifacts to match docs as the
  primary action; documentation should be adjusted to match repository reality.

## Output

Only verified findings with evidence make it to the final report. Do not include intermediate hypotheses or reasoning.
