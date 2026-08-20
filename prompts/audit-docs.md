# Audit Prompt — Stage 1

Plain, tool-agnostic prompt template. Paste one document at a time as
`{{DOCUMENT}}` into any chat LLM, or point an agentic CLI at this file
with the target doc as input.

```
You are auditing a piece of documentation to find everything that makes it
hard for an LLM to *infer* correct answers, as opposed to just retrieve
matching sentences. You are not rewriting anything yet — only diagnosing.

Read the document below and return findings in exactly this structure:

## Undefined or ambiguous terms
List every term, acronym, or concept used but not defined in this doc,
and every term that's defined loosely enough that two readers could
interpret it differently. For each: the term, where it appears, why it's
ambiguous.

## Implicit context
List every place the doc assumes knowledge it doesn't state — references
to "the system," "this case," "as above," a process, or a decision without
explaining what it is. Quote the phrase and say what's missing.

## Buried conditionals
List every rule that is actually conditional ("if X then Y, unless Z")
but is written as flat narrative prose, making the logic implicit rather
than explicit. Quote the passage and restate the logic as an explicit
if/then/unless statement.

## Missing scope or boundaries
Does the doc say what it applies to (version, plan tier, environment,
region, user role, date range)? List any claim made without a stated
scope where scope plausibly matters.

## Missing rationale
List statements that say what to do without saying why. Flag only cases
where the "why" would actually help someone (or a model) correctly
generalize to a similar-but-not-identical situation not covered by the
doc.

## Retrieval-only smells
List anything written in a way that only makes sense as an isolated
search-result snippet (e.g. dangling pronouns, headers that assume the
reader just read the previous section, examples with no stated general
rule behind them).

## Severity ranking
Rank the above findings by how much each one would actually cause an LLM
to give a *wrong* answer to a plausible user question (not just an
incomplete one). Top 5 only.

Be concrete and cite the exact text for every finding. Do not invent
issues that aren't in the text. If a category has no findings, say "none."

DOCUMENT:
{{DOCUMENT}}
```

**Repo usage:** write the output to `docs/_ai-friendly-audit/<doc-path>.audit.md`.
