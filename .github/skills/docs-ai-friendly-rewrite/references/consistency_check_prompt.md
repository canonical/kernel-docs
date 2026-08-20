# Cross-Doc Consistency Check Prompt — Stage 4

Run against a batch of rewritten, related docs together. Fill in
`{{DOCS}}` as a concatenation of the docs, each labeled with its path
and Diátaxis category.

```
You are checking a set of Sphinx/MyST documentation pages (Diátaxis
structure) for cross-document consistency, since inconsistency between
docs is one of the main ways an LLM gives a wrong answer even when each
individual doc looks fine.

For the documents below, find and report:

## Contradictions
Any place where two docs state something incompatible about the same
topic (different versions, different steps, different scope for the
same feature). Quote both passages and name both docs.

## Terminology drift
Any place the same concept is named differently across docs, or a term
defined in the internal working glossary is used with a different
meaning somewhere else.

## Duplicated-but-diverged content
Sections covering the same ground that have drifted apart (one updated,
the other not). Flag which looks more current if determinable,
otherwise flag the pair.

## Broken or vague cross-references
Any {ref}/{doc} or :ref:/:doc: reference that doesn't point to a valid
section-prefixed label, or a "Related topics" entry that no longer
matches the referenced doc's current content.

## Label-prefix inconsistencies
Any cross-reference label that doesn't follow this repo's
section-prefix convention (tutorial-*, how-to-*, exp-*, ref-*) for the
Diátaxis category it's in.

## Coverage gaps
Questions a user could reasonably ask that fall in the gap between two
docs — where each assumes the other covers it, and neither actually
does.

For each finding, state which doc(s) should be corrected and a one-line
suggested fix. Do not rewrite the docs here — just report.

DOCUMENTS:
{{DOCS}}
```

**Repo usage:** write output to
`.github/ai-friendly-audit/consistency-report.md`. Feed each "should be
corrected" item back through `rewrite_prompt.md` for the relevant doc,
then re-run this check on the updated batch until clean. If a fix
involves renaming/moving a page, add the redirect in `docs/conf.py` per
the existing convention.
