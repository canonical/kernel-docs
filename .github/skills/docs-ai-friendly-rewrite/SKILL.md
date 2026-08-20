---
name: docs-ai-friendly-rewrite
description: Rewrite existing documentation so LLMs can reason and infer from it, not just retrieve matching snippets. Use whenever asked to make docs "AI-friendly," "LLM-friendly," or "inference-friendly," to answer questions the docs don't state verbatim, or to audit/rewrite documentation for AI consumption. Applies to this repo's Sphinx/MyST/RST Diátaxis content under docs/.
---

# Docs → AI-Friendly (Inference-Ready) Rewrite

Follows the open Agent Skills format (agentskills.io). This version is
tailored to this repo's conventions in `.github/copilot-instructions.md`
— read that file first; this skill builds on it, not around it.

## The core distinction

**Retrieval-friendly** docs (optimized for search/RAG): short,
self-contained chunks, keyword-rich, one topic per chunk.

**Inference-friendly** docs (optimized for reasoning): explicit
definitions, explicit conditional logic ("if X then Y, unless Z"),
explicit scope/boundaries, consistent terminology across the whole
corpus, and stated rationale — so a model can correctly answer
questions the docs never spell out verbatim.

Most teams only optimize for the first. This skill adds the second, on
top of the first — it's an audit-and-rewrite pass, not a
re-architecture, and it does not change this repo's Diátaxis structure,
formatting rules, or build tooling.

## Repo-specific conventions this workflow uses

- **Internal working glossary**: `.github/ai-friendly-audit/glossary.md`
  — a term-consistency working file for this pipeline only. It is
  separate from `docs/reference/glossary.md`, which is the reader-
  facing glossary and serves a different purpose; this workflow does
  not read, write, or otherwise touch that file. Spelling
  exceptions/valid technical terms still go in
  `docs/.custom_wordlist.txt` as normal.
- **Audit/report output**: `.github/ai-friendly-audit/` — never under
  `docs/`, since anything under `docs/` is picked up by the Sphinx build.
- **Front matter**: don't add new front-matter keys. Keep the required
  MyST/RST meta description front matter untouched.
- **Diátaxis category**: preserve it. A how-to rewritten for clarity is
  still a how-to, not reference material.
- **Formatting**: keep all rules from `copilot-instructions.md` — sentence
  case headings, active voice, blank line after headings/before lists,
  section-prefixed cross-reference labels, no emoji.

## Workflow

### Stage 1 — Audit (per doc)
Run `references/audit_prompt.md` against each document that doesn't
already have an up-to-date audit. Returns structured findings:
undefined terms, implicit assumptions, buried conditionals, missing
scope, missing rationale. Save output to
`.github/ai-friendly-audit/<doc-path>.audit.md` (e.g. for
`docs/how-to/build-kernel.md`, write
`.github/ai-friendly-audit/how-to/build-kernel.audit.md`). Do every doc
before touching any rewrite.

### Stage 2 — Build/update the internal working glossary
Merge every audit's "undefined/ambiguous terms" findings into
`.github/ai-friendly-audit/glossary.md`: canonical term → definition →
doc(s) that currently define or use it inconsistently. This is a
working file for this pipeline's own consistency checks, not
publishable content — it is not `docs/reference/glossary.md` and
nothing here gets merged into that file. Separately, if a term should
also exist in the repo's real reader-facing glossary, flag that as a
normal content suggestion for a human to action, not something this
pipeline does itself. Add new valid technical terms to
`docs/.custom_wordlist.txt` (alphabetically sorted, per existing
convention) as usual. Skip this stage only for a very small,
already-consistent batch of docs.

### Stage 3 — Rewrite (per doc)
Run `references/rewrite_prompt.md` on each audited doc, passing in its
audit file and the current internal working glossary. Output: explicit
conditions, stated scope (in prose, not new front matter), consistent
terminology, rationale added where missing, "Related topics" section
updated if applicable. Rewrite the doc in place, preserving its
Diátaxis category and all existing formatting conventions.

### Stage 4 — Cross-doc consistency check
Run `references/consistency_check_prompt.md` against the *rewritten*
batch. Flags contradictions, drifted duplicate content, orphaned
cross-references, and label-prefix inconsistencies (`tutorial-*`,
`how-to-*`, `exp-*`, `ref-*`). Write to
`.github/ai-friendly-audit/consistency-report.md`. Fix flagged issues,
re-run until clean.

### Stage 5 — Validate
Two checks, both required before a doc counts as done:
1. **Quality gate**: `make spelling`, `make linkcheck`, `make lint-md`,
   `make vale`, `make html` all pass.
2. **Inference test**: maintain
   `.github/ai-friendly-audit/validation-questions.md` — ~15-20
   questions requiring combining or deriving from multiple facts, not
   answerable by single-sentence lookup (e.g. not "what's the default
   build target?" but "if a user is cross-compiling for arm64 and also
   wants to enable KASAN, which steps from the how-to guides apply and
   in what order?"). Run these against the rewritten docs.

## Worked example: unstated capability

This is the pattern most worth watching for, since it's easy to miss —
the doc has every fact needed to answer a derived question, but never
states the implication that connects them.

**Original doc** (`docs/how-to/testing/use-lxd-for-testing.md`, excerpt):

> Launch a container to test your build in isolation:
> ```
> lxc launch ubuntu:noble kernel-test
> ```
> Copy your built kernel package into the container and install it.

**Audit finding** (Stage 1, "Unstated capabilities or implications"):
the image tag (`ubuntu:noble`) sets the container's Ubuntu series
independently of the host machine's installed series. The doc never
says this, so a reader can't infer they could run
`lxc launch ubuntu:jammy kernel-test` to test a Jammy-series kernel
while their host runs Noble. Plausible question this blocks: *"How do
I test a Jammy kernel if I only have Noble installed?"*

**Rewritten doc** (Stage 3): adds one explicit sentence —

> Launch a container to test your build in isolation. The image tag
> (for example `ubuntu:noble`, `ubuntu:jammy`) sets the container's
> Ubuntu series and is independent of your host machine's installed
> series — so you can test a kernel for a different series than the
> one installed on your host:
> ```
> lxc launch ubuntu:noble kernel-test
> ```
> Copy your built kernel package into the container and install it.

**Validated by** (Stage 5): the question "How do I test a Kernel from
the Jammy series? I only have Noble installed" now has a directly
inferable, correct answer from this page alone — `lxc launch
ubuntu:jammy <container-name>` — without the page ever stating that
exact question-and-answer pair verbatim.

## Notes
- Don't run Stage 3 before Stage 2 on a multi-doc corpus — you'll lock
  in inconsistent terminology instead of fixing it corpus-wide.
- If renaming or moving a doc as part of a rewrite, add the redirect in
  `docs/conf.py` per the existing convention — this workflow doesn't
  change that requirement.
- For a single doc, Stages 1 and 3 alone (skip glossary/consistency)
  are enough.
- The three reference prompts are also duplicated as plain files in the
  repo's `prompts/` folder for manual/copy-paste use outside Copilot.
