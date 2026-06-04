---
name: documentation-build
description: "Validates documentation builds successfully. Use when checking Sphinx/RTD build integrity or diagnosing build failures. Reports errors, warnings, and build configuration issues."
---

# Documentation Build Validation

## Scope

Build validation only: detect documentation build configuration, run applicable build targets, collect all errors and warnings, and categorize by severity.

## Inputs

- Repository root.

## Actions

1. **Identify documentation root**: Detect docs roots in this order:

   - `docs/`
   - Repository root, when both `conf.py` and `Makefile` exist
   - `doc/`
   - `documentation/`
   - `site/`
   - `docs-src/`

   If still not found, perform a bounded search for `conf.py` (max depth 4) and use its parent as the docs root.

2. **Detect build configuration**: Check for the presence of:

   - `conf.py` in the detected docs root
   - `Makefile` in the detected docs root
   - Optional: `.readthedocs.yaml` in the detected docs root or at repository root

   If Sphinx build artifacts are absent in the target repository, report "not applicable" in findings and exit cleanly.

3. **Run build targets** (when applicable):

   ```bash
   cd <docs_root>
   # Use clean-doc when available, otherwise fall back to clean
   if make -n clean-doc 2>/dev/null; then
     make clean-doc
   else
     make clean
   fi
   make html
   ```

   Run additional checks for targets that exist.
   Check each target before running to avoid false failures:

   ```bash
   # Check and run each target if available
    for target in spelling linkcheck lint-md vale woke pa11y; do
     if make -n $target 2>/dev/null; then
       make $target
     fi
   done
   ```

4. **Capture output and handle failures**: If any command fails:

   1. Capture the full error output from stderr and stdout
   2. Run `make clean-doc` (or `make clean` if `clean-doc` is unavailable) to reset build state
   3. Retry the failed build command once
   4. If retry fails, STOP and report all captured errors
   5. Do not proceed to content analysis until build succeeds

   Warnings must be collected and reported, but are not blocking unless the repository explicitly treats warnings as errors.

5. **Categorize findings by severity**:

   - **Errors**: Build failures, broken links, missing files.
   - **Warnings**: Deprecation notices, missing references, formatting issues.
   - **Info**: Suggestions, minor notices.

6. **Verify completion**: Confirm the validation completed:

   - Build targets were executed (or determined not applicable)
   - Output was captured (errors and warnings)
   - Findings were categorized by severity

   State the completion status:
   - `✓ Build validation complete: [N] errors, [M] warnings found`
   - OR `✓ Build validation complete: No issues found`
   - OR `✓ Build validation: Not applicable - Sphinx artifacts not detected`

## Constraints

- Do not approve documentation that fails the Sphinx build.
- Build docs locally to catch build warnings.
- Do not invent Makefile targets; only use targets confirmed to exist in the target repository.

## Output

A build validation report listing all errors and warnings, categorized by severity.
If Sphinx artifacts are not detected, report "Not applicable -- Sphinx artifacts not detected in target repo".
