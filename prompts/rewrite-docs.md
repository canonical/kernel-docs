# Rewrite Prompt — Stage 3

Plain, tool-agnostic prompt template. Run per document, after Stage 1
(audit) and Stage 2 (glossary) exist. Fill in `{{DOCUMENT}}`,
`{{AUDIT_FINDINGS}}`, and `{{GLOSSARY}}`.

```
You are rewriting a documentation page so an LLM can reason over it and
correctly infer answers to questions it doesn't state verbatim — while
keeping it just as readable for humans.

Apply these rules:

1. Replace every ambiguous or undefined term (see audit findings and
   glossary below) with the canonical term and, on first use in this
   doc, a one-line inline definition.
2. Rewrite buried conditionals as explicit if/then/unless statements
   or a small decision table, wherever the audit flagged one. Don't
   convert every sentence into a table — only genuinely conditional
   logic.
3. State the scope of every claim that needs one: what version, plan,
   environment, role, or condition it applies to. If scope is unknown,
   say so explicitly rather than leaving it ambiguous — "applies to all
   plans unless noted" is fine; silence is not.
4. Add one line of rationale ("why") next to instructions where the
   audit flagged missing rationale — only where it would help someone
   correctly handle a similar case not explicitly covered.
5. Make the doc self-contained: resolve "as mentioned above" / "in this
   case" into the actual referent, or an explicit link with enough
   context that the sentence still makes sense in isolation.
6. Add a short front-matter block at the top:
   - title
   - applies_to (version/plan/scope)
   - last_reviewed
   - related_docs (canonical titles/links, not just "see also")
7. Keep every fact from the original. Do not invent new facts, numbers,
   or behavior. Do not remove information — only clarify, restructure,
   and make implicit things explicit.
8. Keep existing headers/chunk boundaries where they already work for
   search — this is about adding inference-readiness, not redoing
   information architecture.
9. Use the canonical terminology from the glossary consistently
   throughout, even if the original doc used different words.

At the end, output a short "Changes made" list summarizing what you
clarified, so a human reviewer can spot-check.

AUDIT FINDINGS FOR THIS DOC:
{{AUDIT_FINDINGS}}

CANONICAL GLOSSARY (corpus-wide):
{{GLOSSARY}}

DOCUMENT TO REWRITE:
{{DOCUMENT}}
```

**Repo usage:** `{{AUDIT_FINDINGS}}` = contents of
`docs/_ai-friendly-audit/<doc-path>.audit.md`; `{{GLOSSARY}}` =
contents of `docs/_glossary.md`. Rewrite the doc in place; note any new
or renamed glossary terms in the PR description.
