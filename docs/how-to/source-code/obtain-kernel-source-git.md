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

Each Ubuntu release (e.g. "Noble", "Resolute") has its own codename-based kernel
series and corresponding Git repository.
Use `git clone` with the selected protocol to obtain a local copy of the
kernel source for the Ubuntu kernel series you are interested in.

For example, to obtain a local copy of the Jammy kernel tree, run any of the
following `git clone` commands:

```{code-block} shell
git clone git://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
git clone git+ssh://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
git clone https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
```

See {ref}`exp-ubuntu-kernel-source-protocols` for more information.

## Clone multiple releases using a shared reference repository

Cloning a single kernel tree downloads several hundred megabytes of data.
If you plan to work with more than one Ubuntu kernel series, clone the upstream
Linux kernel repository first and use it as a reference repository for the
subsequent Ubuntu clones.
This saves time and disk usage by reducing duplicate downloads.

```{code-block} shell
git clone https://kernel.ubuntu.com/ubuntu/linux.git
git clone --reference linux https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
git clone --reference linux https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/noble
```

Each Ubuntu `git clone` creates a separate directory for a given series and has
the full source and history available locally.

```{caution}
Once two trees are linked this way, you cannot delete or move the upstream
`linux` reference tree without manually updating `.git/objects/info/alternates`
in each Ubuntu kernel tree that references it.
```

## Add multiple series as remotes

If you want to compare or switch between several Ubuntu kernel series in one
working repository, add each series as a remote and switch between them using
branches.
This keeps the series in one repository, but makes its remote and branch
structure more complex than using separate clones:

```{code-block} shell
git remote add jammy https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
git fetch jammy
git checkout -b jammy --track jammy/master
git checkout -b jammy-next --track jammy/master-next
```

For example, if you want to check out the current Ubuntu kernel source for
Jammy, use the `jammy` branch, which tracks `master`.
If you instead want to check out the commits staged for the next Stable Release
Update (SRU), you can create the `jammy-next` branch, which tracks
`master-next`. 

## Work with multiple series in separate subdirectories

If you need the source for each Ubuntu kernel series in its own subdirectory
within one repository, use `git subtree add`. This layout is useful when the
series should be visible together in one working tree, but it puts the large
kernel histories into that repository and requires explicit update commands.

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

By default, cloning checks out the repository's default branch, which is
`master` for the Ubuntu kernel repositories described here. To work with a
specific, previously released kernel version, use an Ubuntu release tag. An
Ubuntu release tag starts with `Ubuntu-` and identifies a released kernel
version.

To list matching tags in the cloned repository:

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

To check out a specific version while keeping a branch for additional local
commits, create a branch pointing to that tag:

```{code-block} shell
git checkout -b temp Ubuntu-5.4.0-52.57
```

The new branch points to the tagged snapshot, so you can add commits without
leaving the repository in a detached `HEAD` state.

## Related topics

- {doc}`/explanation/ubuntu-linux-kernel-sources`

% LINKS

[git package]: https://packages.ubuntu.com/search?keywords=git
