# Kernel Team Internal Documentation - Copilot Instructions

## Project Overview

This is the **Kernel team's internal documentation** - a Sphinx-based documentation project using the [Canonical Sphinx Stack](https://github.com/canonical/sphinx-stack).
Documentation targets the kernel team's documentation processes, standards, and best practices for maintaining the Ubuntu kernels.

### Repository scope

This is a docs-only repository.
It contains documentation content and documentation tooling only.
There is no product runtime or application source code in scope for behavior verification.

When verifying documentation accuracy, treat repository artifacts as the source of truth:
`docs/conf.py`, `docs/Makefile` targets, Sphinx configuration, examples, redirects,
and consistency across documentation pages.

## Architecture & Structure

### Diátaxis Framework

Content is organized using the [Diátaxis framework](https://diataxis.fr/):

- `tutorial/` - Getting started guides (for example, `crank-your-first-kernel.md`).
- `how-to/` - Task-oriented guides organized by topic or stages of kernel development (for example, stable updates, testing, and development).
- `explanation/` - Conceptual overviews and background information.
- `reference/` - Technical specifications, glossaries, and system requirements.

### File Types

- **Markdown (`.md`)** - Primary format for content pages with MyST syntax support.
- **reStructuredText (`.rst`)** - Landing pages, index files, and content pages.
- Mixed content: both formats coexist and are processed by Sphinx.

### Repository layout

- `docs/` - Documentation root.
- `docs/tutorial/` - Tutorials and onboarding guides.
- `docs/how-to/` - Task-oriented operational guides.
- `docs/explanation/` - Conceptual and background documentation.
- `docs/reference/` - Specifications, glossary entries, and reference material.
- `docs/reuse/` - Shared links and reusable documentation snippets.
- `docs/conf.py` - Sphinx project configuration, including redirects.
- `docs/Makefile` - Documentation build, test, and local serve targets.

### Key Configuration Files

- `docs/conf.py` - Project-specific settings.
- `docs/Makefile` - Build system.
- `docs/.readthedocs.yaml` - Read the Docs build configuration.

## Development Workflow

### Local Setup

```bash
git clone https://github.com/canonical/kernel-docs.git
cd kernel-docs/docs
sudo apt update
sudo apt install make python3 python3-venv python3-pip
make install
```

### Build & Preview

```bash
make run          # Build, watch, and serve at http://127.0.0.1:8000
make html         # Build only
make serve        # Serve only
make clean-doc    # Clean built files
```

For remote/VM development, set `export SPHINX_HOST=0.0.0.0` before running `make run`.

### Testing & Quality Checks

```bash
make spelling     # Spell check (uses .custom_wordlist.txt for exceptions)
make linkcheck    # Verify all links
make lint-md      # Check Markdown formatting and MyST syntax
make vale         # Check style guide compliance (Canonical Vale rules)
make html         # Build docs and surface Sphinx warnings/errors
make woke         # Check inclusive language
make pa11y        # Accessibility testing
```

During development, run the checks that match the files you changed.
Before submitting a PR, always run `make spelling`, `make linkcheck`, `make lint-md`, `make vale`, and `make html`.

## Writing Conventions

### Style & Language

- Follow the [Canonical documentation style guide](https://docs.ubuntu.com/styleguide/en).
- Use **US English** (`en-US`).
- Acronyms: expand on first use, for example, "Yet Another Markup Language (YAML)."
- Add technical terms to `docs/reference/glossary.md` and spell exceptions to `docs/.custom_wordlist.txt`.

### Cross-References

- Prefix all labels with the Diátaxis section to avoid clashes across pages.
  - Recommended short prefixes: `tutorial-*`, `how-to-*`, `exp-*`, `ref-*`.
- In `.rst` files, define labels with section-prefixed names:
  - `.. _how-to-label:`
- In `.rst` files, link with `:ref:\`label-name\`` and `:doc:\`/path/to/page\`` for internal pages.
- In `.md` (MyST) files, define labels near the top of the page with section-prefixed names:
  - `(how-to-label)=`
- In `.md` (MyST) files, use `{ref}` for labels and `{doc}` for internal page links.
- Prefer native internal cross-references (`:ref:`, `:doc:`, `{ref}`, `{doc}`) over plain relative links so broken links surface during `make run` and `make html`.
- First mentions of packages and tools should link to official documentation or manpages.
- Use semantic markup: `{kbd}\`Ctrl\``, `{manpage}\`dpkg(1)\``, `{term}\`DAC\``.
- Manpage links auto-generate URLs (no hardcoding needed).

### Formatting Rules

- Blank line required after every heading before content.
- Blank line required before every list (bullet or numbered).
- Use sentence case for headings, not title case.
- Active voice preferred: "This command does X" not "X is done by this command".
- In `.md` files, use MyST admonition syntax: `` ```{note} ``, `` ```{warning} ``, `` ```{important} ``.
- In `.rst` files, use RST admonition syntax: `.. note::`, `.. warning::`, `.. important::`.

### Markdown Elements

- **Headings**: Use proper hierarchy (`#`, `##`, `###`, `####`); don't skip levels.
- **Lists**: Use `1.` for all numbered items (auto-renumbers).
- **Code blocks**: Specify language for syntax highlighting.
- **MyST extensions**: `attrs_block`, `attrs_inline`, `colon_fence`, `deflist`, `substitution`.

### File Structure

- Content pages are referenced once via their section landing page.
- Landing pages in `docs/how-to/`, `docs/tutorial/`, and related sections organize navigation.
- Images are stored in `docs/<section>/images/` directories.
- Shared links are defined in `docs/reuse/links.txt` and auto-included via `rst_epilog`.

## Critical Patterns

### Redirects

When renaming/moving/deleting files, **always add redirects**:

**Add redirects in `docs/conf.py` under `redirects = {}`**:

```python
redirects = {
  # Internal redirect (full docs path)
  "how-to/old-page": "how-to/new-page",
  # External redirect (full URL)
  "how-to/obsolete-page": "https://example.com/new-location",
}
```

### Custom Wordlist

Add valid technical terms/acronyms to `docs/.custom_wordlist.txt` (alphabetically sorted) rather than wrapping in backticks, unless you want monospaced rendering.

### PR Requirements

- Link PRs to issues with `Fixes #<issue-number>` in the description.
- Use [Conventional Comments](https://conventionalcomments.org/) for feedback.
- Include manual testing for documentation workflows and commands.
- Preview builds are available via the Read the Docs check on the PR.

## Common Tasks

### Meta Description Format

All pages must have an HTML meta description. The format depends on file type:

**MyST Markdown** (`.md`): Add to the front matter at the top of the file:

```yaml
---
myst:
  html_meta:
    description: "Brief, user-facing description of the page content (50-160 characters)."
---
```

**reStructuredText** (`.rst`): Add as a directive at the top of the file before the first heading:

```rst
.. meta::
   :description: Brief, user-facing description of the page content (50-160 characters).
```

Metadata descriptions help with search results and accessibility. Keep them concise and action-oriented.

### Adding New Content

1. Determine Diátaxis category (tutorial/how-to/explanation/reference)
2. Create `.md` / `.rst` file in appropriate subdirectory
3. Add or review the page meta description (see [Meta Description Format](#meta-description-format) above):

  - New files: must include a meta description
  - Existing files: add one if missing, otherwise review and update it if it no longer matches the page intent

4. Add to corresponding `index.rst` / `index.md` or section landing page
5. Use section-prefixed labels / targets for cross-references in both MyST and RST
   For example `(how-to-topic-name)=` in MyST or `.. _how-to-topic-name:` in RST
6. Test: `make run` and verify navigation, formatting, and cross-references work as expected
7. Run quality checks before committing:

  ```bash
  make spelling
  make linkcheck
  make lint-md
  make vale
  make html
  ```

  Fix any warnings or errors reported by these commands.
8. Submit PR with clear description and link to any related issues

Use short section prefixes for anchors when naming labels, for example `tutorial-*`, `how-to-*`, `exp-*`, and `ref-*`.

### Updating Links

- Prefer reputable sources (official upstream documentation, not blog posts).
- Use "Related topics" sections for supplementary links at the end of the page.
- The first package mention should link to documentation or manpages.

### Handling Errors

- **Spelling errors**: Add to `docs/.custom_wordlist.txt` or wrap in backticks.
- **Link errors**: Check `linkcheck_ignore` in `docs/conf.py`.
- **Build errors**: Check `docs/.sphinx/venv/pip_install.log` for dependency issues.
- **Sphinx warnings**: Run `make html` and resolve missing references, syntax issues, and other warnings before merge.

## Don't Do This

- Don't use emojis in documentation.
- Don't skip heading levels in document structure.
- Don't assume reader knowledge without brief explanations or links.
- Don't link to blog posts when official docs exist.
- Don't treat this repository as a mixed code-and-docs project.
