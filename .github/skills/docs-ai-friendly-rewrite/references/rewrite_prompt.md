# Rewrite Prompt — Stage 3

Run per document, after Stage 1 (audit) and Stage 2 (glossary update)
are done. Fill in `{{DOCUMENT}}`, `{{CATEGORY}}`, `{{AUDIT_FINDINGS}}`,
and `{{GLOSSARY}}`.

```
You are rewriting a page from a Sphinx/MyST (or RST) documentation set
so an LLM can reason over it and correctly infer answers to questions
it doesn't state verbatim — while keeping it just as readable for
humans and fully compliant with this repo's existing conventions.

This page's Diátaxis category is: {{CATEGORY}}. Preserve that category
— a how-to must stay task-oriented, reference stays specification-only,
explanation stays conceptual, tutorial stays procedural. Do not blur
categories while clarifying.

Apply these rules:

1. Replace every ambiguous or undefined term (see audit findings and
   internal working glossary below) with the canonical term, and give a
   one-line inline definition on first use in this doc. This working
   glossary is separate from docs/reference/glossary.md (a different,
   reader-facing file this workflow does not touch) — do not add or
   suggest entries there.
2. Rewrite buried conditionals as explicit if/then/unless statements or
   a small table, wherever the audit flagged one — mainly relevant for
   how-to and reference pages. Don't convert every sentence into a
   table.
3. State the scope of every claim that needs one (kernel version,
   architecture, Ubuntu release, environment) inline in prose near the
   relevant content. Do not add new front-matter fields for this.
4. Add one line of rationale ("why") next to instructions where the
   audit flagged missing rationale — only where it helps someone
   correctly handle a similar case not explicitly covered.
5. Where the audit flagged an unstated capability or implication, add
   an explicit sentence spelling it out — phrased so it also answers
   the plausible derived question the audit identified. Only state
   capabilities the doc's own mechanism actually supports; do not
   extrapolate beyond what's verifiably true.
6. Make the doc self-contained: resolve "as mentioned above" / "in this
   case" into the actual referent, or a proper {ref}/{doc} cross-
   reference (MyST) or :ref:/:doc: (RST) per this repo's convention,
   with enough surrounding context that the sentence still makes sense
   on its own.
7. Do NOT touch the existing meta description front matter beyond
   verifying it's still accurate to the rewritten content — update the
   description text only if the rewrite changed what the page is about.
8. If new cross-references were added, use section-prefixed labels
   (tutorial-*, how-to-*, exp-*, ref-*) per the existing convention. If
   this page should link to related pages that weren't linked before,
   add or update its "Related topics" section rather than inventing a
   new field.
9. Keep every fact from the original. Do not invent new facts, numbers,
   or behavior. Do not remove information — only clarify, restructure,
   and make implicit things explicit.
10. Keep existing headings, structure, and all formatting rules from
    this repo's copilot-instructions.md (sentence case headings, active
    voice, blank line after headings/before lists, no emoji, no skipped
    heading levels).

At the end, output two things separately:
- The rewritten document.
- A "Changes made" list, and a "New/updated terms" list (term +
  definition) for this pipeline's internal working glossary only.

AUDIT FINDINGS FOR THIS DOC:
{{AUDIT_FINDINGS}}

CURRENT INTERNAL WORKING GLOSSARY:
{{GLOSSARY}}

DOCUMENT TO REWRITE ({{CATEGORY}}):
{{DOCUMENT}}
```

**Repo usage:** `{{AUDIT_FINDINGS}}` = contents of the matching file in
`.github/ai-friendly-audit/`; `{{GLOSSARY}}` = contents of
`.github/ai-friendly-audit/glossary.md`. Rewrite the doc in place.
Merge the "New/updated terms" list into
`.github/ai-friendly-audit/glossary.md` (Stage 2), and run `make
spelling`, `make linkcheck`, `make lint-md`, `make vale`, `make html`
before considering the doc done.
