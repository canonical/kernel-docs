# How to contribute to Kernel documentation

We believe that everyone has something valuable to contribute, whether you're a
coder, a writer, or a tester. Here's how and why you can get involved:

- **Why join us?** Work with like-minded people, develop your skills, connect
with diverse professionals, and make a difference.
- **What do you get?** Personal growth, recognition for your contributions,
early access to new features, and the joy of seeing your work appreciated.
- **Start early, start easy**: Dive into code contributions, improve
documentation, or be among the first testers. Your presence matters, regardless
of experience or the size of your contribution.

The guidelines below will help keep your contributions effective and meaningful.

## Code of conduct

When contributing, you must abide by the [Ubuntu Code of Conduct].

## License and copyright

By default, all contributions to Kernel documentation are licensed under the
Creative Commons Attribution-Share Alike {spellexception}`(CC-BY-SA)` 3.0
Unported License.
To view a copy of this license, visit
https://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco,
California, 94105, USA.

All contributors must sign the [Canonical contributor license agreement], which
grants Canonical permission to use the contributions. The author of a change
remains the copyright owner of their code (no copyright assignment occurs).

## Environment setup

Kernel documentation is built on top of [Canonical's Sphinx starter pack] and
hosted on [Read the Docs].

To work on the project, you will need to have Python, `python3.12-venv`, and
`make` packages installed.

```{code-block} none
sudo apt install make
sudo apt install python3
sudo apt install python3.12-venv
```

## Documentation

The documentation source files are stored in the `docs` directory of the
repository.

For general guidance, refer to the [starter pack guide](https://canonical-starter-pack.readthedocs-hosted.com/latest/).

For syntax help and guidelines, refer to the [Canonical documentation style guides](https://docs.ubuntu.com/styleguide/en/).

In structuring, the documentation employs the [Diátaxis](https://diataxis.fr/) approach.

To run the documentation locally before submitting your changes:

```bash
make run
```

### Automatic checks

GitHub runs automatic checks on the documentation to verify spelling, validate
links, and suggest inclusive language.

You can (and should) run the same checks locally before committing and pushing
a change:

```bash
make spelling
make linkcheck
make woke
```

## Submissions

If you want to address and issue or bug in this project, leave a comment in the
issue indicating your intent to work on it. Also, reference the issue when you
submit the changes.

- (Kernel docs members) Create a branch off the `main` branch of the
[Kernel documentation GitHub repository] and add your changes to it.

- (External contributors) Fork the [Kernel documentation GitHub repository] and
add the changes to your fork.

- Properly structure your commits, provide detailed commit messages, and
{ref}`sign off your commits <how-to-contribute-sign-off-commits>`.

- Make sure the updated project builds and runs without warnings or errors; this
includes linting, documentation, code (where applicable), and tests.

- Submit the changes as a [pull request (PR)].

Your changes will be reviewed in due time; if approved, they will eventually be
merged.

### Describing pull requests

To be properly considered, reviewed, and merged, your pull request must provide
the following details:

- **Title**: Summarize the change in a short, descriptive title.
- **Description**: Explain the problem that your pull request solves. Mention
any new features, bug fixes, or refactoring.
- **Relevant issues**: Reference any [related issues, pull requests, and repositories].
- **Testing**: Explain whether new or updated tests are included.
- **Reversibility**: If you propose decisions that may be costly to reverse,
list the reasons and suggest steps to reverse the changes if necessary.

### Commit structure and messages

Use separate commits for each logical change, and for changes to different
sections in the Kernel documentation.
Prefix your commit messages with the names of sections or pages that they
affect, using the code tree structure. For example, start a commit that updates
the explanation page about SRU cycles with `explanation/about-sru:`.

Use [conventional commits] to ensure consistency across the project:

```none
docs(how-to/get-sources): Update generic format for source package repository

* Added new URL structure details for Noble: https://github.com/canonical/kernel-docs/issues/12345
* Separate content for pre- and post-24.04 release
```

Such structure makes it easier to review contributions and simplifies porting
fixes to other branches.

(how-to-contribute-sign-off-commits)=
### Sign off on commits

All changes that go into the Kernel documentation repository need to be signed
off (using the `-s` or `--signoff` option) by the contributor.

```{code-block} none
git commit -s -m "docs(explanation/about-sru): updated life cycle diagram"
```

This sign off confirms that you made the changes or have the right to commit it
as an open-source contribution.

If you made a commit without signing off, you can run the following to amend
the most recent commit, append the "Signed-off-by" line without changing the
commit message, and push again:

   ```{code-block} none
   git commit --amend --no-edit -n -s
   git push --force
   ```

<!--
## Code

### Formatting and linting

Kernel documentation relies on these formatting and linting tools:

- [TODO: Tool 1](http://example.com)
- [TODO: Tool 2](http://example.com)

To configure and run them:

```bash
TODO: lint command 1
TODO: lint command 2
```

### Structure

- **Check linked code elements**: Ensure coupled code elements, files, and directories are adjacent. For instance, store test data close to the corresponding test code.
- **Group variable declaration and initialisation**: Declare and initialise variables together to improve code organisation and readability.
- **Split large expressions**: Break down large expressions into smaller self-explanatory parts. Use multiple variables where appropriate to make the code more understandable and choose names that reflect their purpose.
- **Use blank lines for logical separation**: Insert a blank line between two logically separate sections of code to improve its structure and readability.
- **Avoid nested conditions**: Avoid nesting conditions to improve readability and maintainability.
- **Remove dead code and redundant comments**: Drop unused or obsolete code and comments to promote a cleaner code base and reduce confusion.
- **Normalise symmetries**: Treat identical operations consistently, using a uniform approach to improve consistency and readability.

### Best practices

## Tests

All code contributions must include tests.

To run the tests locally before submitting your changes:

```bash
TODO: test command 1
TODO: test command 2
```

-->

## Start contributing

If you are ready to contribute but unsure where to start, here are some
suggested starting points.

1. Pick up an existing [GitHub Issue].

   Whether you're a seasoned pro, or just beginning your journey in kernel
   development and/or open source, there's always a variety of tasks for your
   unique skills. Find an open issue that sparks your interest, assign it to
   yourself, and start collaborating.

1. Update and remove old documentation.

   If you browse through the project and find information or whole pages that
   are either outdated or obsolete, submit a PR with changes to update or delete
   them.

1. Migrate content from Ubuntu Wiki.

   In an effort to make collaboration efforts more effective, and keep content
   accurate and up-to-date, we aim to migrate as much content to our Read the
   Docs instance. If you come across an article that is useful and relevant,
   migrate the content from Wiki by creating a new file and/or section in this
   repository.

1. Work with what's in front of you.

   If none of the earlier suggestions appeal to you, then just browse through
   the existing Kernel documentation with an open mind and keen eye. If you see
   a paragraph that can be written in a more concise manner, or a set of
   instructions that can be made clearer, send along your suggestions for these
   improvements. Big or small, an improvement is always a step in the right
   direction.

Thank you, and looking forward to your contributions!
   

<!-- LINKS -->

[Ubuntu Code of Conduct]: https://ubuntu.com/community/docs/ethos/code-of-conduct
[Canonical contributor license agreement]: https://canonical.com/legal/contributors
[Canonical's Sphinx starter pack]: https://github.com/canonical/sphinx-docs-starter-pack
[Read the Docs]: https://about.readthedocs.com/
[Kernel documentation GitHub repository]: https://github.com/canonical/kernel-docs
[pull request (PR)]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork
[related issues, pull requests, and repositories]: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls
[conventional commits]: https://www.conventionalcommits.org/
[GitHub Issue]: https://github.com/canonical/kernel-docs/issues
