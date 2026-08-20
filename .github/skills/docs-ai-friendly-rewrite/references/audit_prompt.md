# Audit Prompt — Stage 1

Paste one document at a time as `{{DOCUMENT}}`. Note which Diátaxis
category it's in (`tutorial`, `how-to`, `explanation`, `reference`) as
`{{CATEGORY}}` — expectations differ slightly by category (see below).

```
You are auditing a page from a Sphinx/MyST documentation set (Diátaxis
structure) to find everything that makes it hard for an LLM to *infer*
correct answers, as opposed to just retrieve matching sentences. You are
not rewriting anything yet — only diagnosing.

This page's Diátaxis category is: {{CATEGORY}}. Weight your findings
accordingly: undefined terms and buried conditionals matter most in
how-to and reference content; a tutorial is allowed to be procedural
and linear without much conditional branching — don't flag that as a
defect.

Read the document below and return findings in exactly this structure:

## Undefined or ambiguous terms
List every term, acronym, or concept used but not defined in this doc,
plus every term defined loosely enough that two readers could interpret
it differently. For each: the term, where it appears, why it's
ambiguous.

## Implicit context
List every place the doc assumes knowledge it doesn't state — references
to "the system," "this case," "as above," a process, or a decision
without explaining what it is. Quote the phrase and say what's missing.

## Buried conditionals
List every rule that is actually conditional ("if X then Y, unless Z")
but is written as flat narrative prose, making the logic implicit rather
than explicit. Quote the passage and restate the logic as an explicit
if/then/unless statement.

## Missing scope or boundaries
Does the doc say what it applies to (kernel version, architecture,
Ubuntu release, environment)? List any claim made without stated scope
where scope plausibly matters.

## Missing rationale
List statements that say what to do without saying why. Flag only cases
where the "why" would help someone (or a model) correctly generalize to
a similar-but-not-identical situation not covered by the doc.

## Unstated capabilities or implications
List any place the doc demonstrates or references a mechanism,
parameter, flag, or option (e.g. an image tag, a config value, a
command argument) without stating a non-obvious capability that
follows from it — something true and supported, but that a reader
would have to infer rather than find stated, and likely wouldn't think
to ask about directly. For each: the mechanism as shown in the doc, the
unstated capability it implies, and a plausible question a user might
ask that the doc could answer if this were made explicit. Only flag
real, supported implications — do not invent capabilities the doc
doesn't actually support.

Example (do not use this in an unrelated doc, it's illustrative): a
how-to shows `lxc launch ubuntu:noble test-container` as one example
command with no further comment. It never states that the image tag
sets the container's Ubuntu series independently of the host's
installed series — so a reader can't infer from this page alone that
they could run `lxc launch ubuntu:jammy test-container` to test a
Jammy-series kernel on a Noble host. That's a real capability the doc
enables but never says, and it's exactly the kind of question ("how do
I test Jammy if I only have Noble installed?") a user is likely to ask
that the model can't answer without it being explicit.

## Retrieval-only smells
List anything written in a way that only makes sense as an isolated
search-result snippet (dangling pronouns, headers assuming the reader
just read the previous section, examples with no stated general rule
behind them).

## Severity ranking
Rank the above findings by how much each would actually cause an LLM to
give a *wrong* answer to a plausible user question (not just an
incomplete one). Top 5 only.

Be concrete and cite the exact text for every finding. Do not invent
issues that aren't in the text. If a category has no findings, say
"none."

DOCUMENT ({{CATEGORY}}):
{{DOCUMENT}}
```

**Repo usage:** write output to
`.github/ai-friendly-audit/<doc-path-relative-to-docs>.audit.md`.
