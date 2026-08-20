# AGENTS.md

`AGENTS.md` is a shared convention read by most coding agents (GitHub
Copilot coding agent, Codex, Cursor, Claude Code, Amp, and others) — no
tool-specific setup needed for this file itself. See
`.github/copilot-instructions.md` for this repo's full documentation
conventions (Diátaxis, Sphinx/MyST formatting, cross-references, PR
requirements) — this file only covers the AI-inference-friendliness
pipeline on top of those.

## Docs AI-friendliness pipeline

Full stage instructions live in
`.github/skills/docs-ai-friendly-rewrite/SKILL.md` and its
`references/` prompts (also duplicated as plain files in `prompts/`).

### Persistent state

- `.github/ai-friendly-audit/glossary.md` — internal working glossary
  for this pipeline's own term-consistency checks. Separate from, and
  never merged into, `docs/reference/glossary.md`, which is the
  reader-facing glossary and serves a different purpose.
- `docs/.custom_wordlist.txt` — existing spelling-exceptions file; new
  valid technical terms go here too.
- `.github/ai-friendly-audit/<doc-path>.audit.md` — audit findings per
  source doc, mirroring its path under `docs/`. Kept outside `docs/` so
  the Sphinx build never picks it up.
- `.github/ai-friendly-audit/consistency-report.md` — latest cross-doc
  consistency check.
- `.github/ai-friendly-audit/validation-questions.md` — held-out
  inference-question test set (Stage 5). Append over time; don't delete
  existing questions without flagging it in the PR.

### Pipeline

1. **Audit** every doc that doesn't have an up-to-date `.audit.md` (or
   that changed since its last audit). Criteria:
   `.github/skills/docs-ai-friendly-rewrite/references/audit_prompt.md`.
2. **Update the internal working glossary**: merge audit findings'
   undefined-term lists into `.github/ai-friendly-audit/glossary.md`
   (this pipeline's own file — never `docs/reference/glossary.md`); add
   recurring valid technical terms to `docs/.custom_wordlist.txt`.
3. **Rewrite** each audited doc in place. Criteria:
   `.github/skills/docs-ai-friendly-rewrite/references/rewrite_prompt.md`.
   Preserve Diátaxis category, all existing formatting rules, and every
   fact from the original.
4. **Consistency check** the rewritten batch. Criteria:
   `references/consistency_check_prompt.md`. Fix flagged issues, re-run
   until clean.
5. **Validate**: (a) `make spelling`, `make linkcheck`, `make lint-md`,
   `make vale`, `make html` all pass; (b) rewritten docs correctly
   answer the held-out inference questions in
   `validation-questions.md`.

### PR conventions (same as this repo's existing conventions)

- Link PRs to issues with `Fixes #<issue-number>`.
- Use Conventional Comments for review feedback.
- One PR per batch of related docs, not the whole repo at once.
- PR description includes: docs audited/rewritten, any new glossary
  terms added, and consistency-check results.
- If a rewrite renames/moves a page, add the redirect in `docs/conf.py`
  per the existing convention.
- Preview build via the Read the Docs check on the PR, same as any
  other doc change.

## Using this with a specific tool

The pipeline works by having any agent read
`.github/skills/docs-ai-friendly-rewrite/SKILL.md` and act on it, or by
pasting files from `prompts/` into a chat by hand.

- **GitHub Copilot (Visual Studio / VS Code / JetBrains)**: the skill
  under `.github/skills/` auto-discovers; `.github/copilot-instructions.md`
  provides always-on baseline context.
- **Claude / Claude Code**: copy
  `.github/skills/docs-ai-friendly-rewrite/` into `.claude/skills/`
  (project) or `~/.claude/skills/` (personal) — same SKILL.md, no
  changes needed.
- **Other agentic CLIs**: point the tool at this `AGENTS.md`, or pass a
  file from `prompts/` directly as a prompt.
- **No agent tooling**: open a file from `prompts/`, paste into any
  chat LLM, fill in the placeholders by hand.
