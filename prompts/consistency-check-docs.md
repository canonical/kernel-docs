# Cross-Doc Consistency Check Prompt — Stage 4

Plain, tool-agnostic prompt template. Run against a batch of rewritten,
related docs together (not one at a time — this stage needs cross-doc
visibility). Fill in `{{DOCS}}` as a concatenation of the docs, each
clearly labeled with its title/path.

```
You are checking a set of documentation pages for cross-document
consistency, since inconsistency between docs is one of the main ways
an LLM gives a wrong answer even when each individual doc looks fine.

For the documents below, find and report:

## Contradictions
Any place where two docs state something incompatible about the same
topic (different numbers, different rules, different scope for the
same feature). Quote both passages and name both docs.

## Terminology drift
Any place where the same concept is named differently across docs, or
where a term defined in one doc is used with a different meaning in
another.

## Duplicated-but-diverged content
Sections that clearly cover the same ground but have drifted apart
(one was updated, the other wasn't). Flag which one looks more current
if there's a dated field, otherwise just flag the pair.

## Broken or vague cross-references
Any "see [doc]" or similar reference that doesn't point to something
findable, or that used to make sense but no longer matches the
referenced doc's current content.

## Coverage gaps
Questions a user could reasonably ask that fall in the gap between two
docs — where each doc assumes the other one covers it, and neither
actually does.

For each finding, state which doc(s) should be corrected and a one-line
suggested fix. Do not rewrite the docs here — just report.

DOCUMENTS:
{{DOCS}}
```

**Repo usage:** write output to
`docs/_ai-friendly-audit/consistency-report.md`. Feed each "should be
corrected" item back through `rewrite_prompt.md` for the relevant doc
(add the fix as an extra audit-findings bullet), then re-run this check
on the updated batch until clean.
