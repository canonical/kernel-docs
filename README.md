# kernel-docs

The Kernel documentation is about the Ubuntu Linux kernel, mainly focused on its
development processes, tools, schedules, and more.

## Documentation

This project is built with Sphinx and hosted on Read the Docs.

View the documentation site at: https://canonical-kernel-docs.readthedocs-hosted.com/en/latest/

## Contribute

New documentation, fixes, and updates are greatly appreciated. Be sure to read
our [contribution guidelines](docs/how-to/contribute.md) first.

## Using Copilot instructions

This repository includes guidance for GitHub Copilot in
[.github/copilot-instructions.md](.github/copilot-instructions.md).

Copilot should follow these repository instructions when suggesting edits,
reviews, and documentation checks.

### Copilot in VS Code

1. Open this repository in VS Code.
1. Use Copilot Chat and ask it to follow
   [.github/copilot-instructions.md](.github/copilot-instructions.md).
1. For documentation work, target files under `docs/`.

Example prompt:

> Follow .github/copilot-instructions.md and review docs/how-to/contribute.md.

### Copilot CLI

The Copilot instructions file is a policy/reference file and is not executed.

If your CLI workflow does not auto-load repository instructions, reference
[.github/copilot-instructions.md](.github/copilot-instructions.md)
explicitly in your prompt.

Example:

```bash
gh copilot suggest "Follow .github/copilot-instructions.md and suggest improvements for docs/how-to/contribute.md"
```

## Use Copilot Skills

For comprehensive documentation reviews, use the documentation-review skill:

- Skill file:
  [.github/skills/documentation-review/SKILL.md](.github/skills/documentation-review/SKILL.md)
- Coverage: build validation, structure discovery, Diataxis classification,
  structure audit, accuracy verification, style review, and consolidated report.

Prompt example:

> Follow .github/copilot-instructions.md. Run the documentation-review skill from SKILL.md on docs/how-to/contribute.md only.
