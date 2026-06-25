---
myst:
  html_meta:
    description: "Obtain and manage Ubuntu kernel source code using Git. Guide for cloning kernel repositories for one or more Ubuntu releases, working with subtrees, tags, and more."
---

# How to obtain and manage kernel source for an Ubuntu release using Git

The kernel source code for each Ubuntu release is maintained in its own
repository in Launchpad. Downloading the kernel source may be needed for
customization, development, or troubleshooting the kernel.

This document shows how you can obtain and manage the kernel source for an
Ubuntu release using Git.

## Prerequisites

You must have the [git package] installed on your system.

```{code-block} shell
sudo apt-get install git
```

## Get local copy of kernel source for single release

You can use `git clone` with the selected protocol to obtain a local copy of
the kernel source for the release you are interested in.

For example, to obtain a local copy of the Jammy kernel tree, run any of the
following `git clone` commands:

```{code-block} shell
git clone git://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
git clone git+ssh://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
git clone https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
```

See {ref}`exp-ubuntu-kernel-source-protocols` for more information.

## Clone multiple releases using a shared reference repository

Cloning a single kernel tree downloads several hundred megabytes of data. If
you plan to work with more than one kernel release, you can save space and time
by first downloading the upstream kernel tree and using it as a reference for
subsequent clones:

```{code-block} shell
git clone https://kernel.ubuntu.com/ubuntu/linux.git
git clone --reference linux https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
git clone --reference linux https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/noble
```

Each `git clone` creates a new directory for a given release, containing the full source and history of the repository.

```{caution}
Once two trees are linked this way, you cannot delete or move the upstream
`linux` reference tree without manually updating
`.git/objects/info/alternates` in each Ubuntu kernel tree that references it.
```

## Add multiple series as remotes

If you are an advanced Git user, you can add each Ubuntu series as a remote to
have all kernel series in a single Git repository, and switch between them
using branches:

```{code-block} shell
git remote add jammy https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
git fetch jammy
git checkout -b jammy --track jammy/master
git checkout -b jammy-next --track jammy/master-next
```

## Work with multiple series in separate subdirectories

To have the source for each kernel series available in its own subdirectory
within a single Git repository, use `git subtree add`:

```{code-block} shell
git subtree add --prefix=jammy https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy master
git subtree add --prefix=noble https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/noble master
```

This creates a `jammy/` subdirectory containing the Jammy kernel source and a
`noble/` subdirectory containing the Noble kernel source, all within the same
repository.

To pull future updates into a subtree, specify the remote URL and ref
explicitly - there is no automatic upstream tracking for subtrees:

```{code-block} shell
git subtree pull --prefix=jammy https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy master
```

## Work with a specific kernel version using tags

By default, cloning gives you the latest state of the `master` branch. To work
with a specific, previously released kernel version, use release tags. To list
all available tags for a release:

```{code-block} shell
git tag -l Ubuntu-*
```

Example output:

```{code-block} text
Ubuntu-5.4.0-47.51
Ubuntu-5.4.0-48.52
Ubuntu-5.4.0-49.53
Ubuntu-5.4.0-51.56
Ubuntu-5.4.0-52.57
...
```

To check out a specific version, create a branch pointing to that tag:

```{code-block} shell
git checkout -b temp Ubuntu-5.4.0-52.57
```

You can then work with that version - for example, by adding new commits.

## Related topics

- {doc}`/explanation/ubuntu-linux-kernel-sources`
- <https://wiki.ubuntu.com/Kernel/Dev/KernelGitGuide>

% LINKS

[git package]: https://packages.ubuntu.com/search?keywords=git
