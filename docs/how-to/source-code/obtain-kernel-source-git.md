# How to obtain kernel source for an Ubuntu release using Git

The kernel source code for each Ubuntu release is maintained in its own
repository in Launchpad. Downloading the kernel source may be needed for
customization, development, or troubleshooting the kernel.

This document shows how you can obtain the kernel source for an Ubuntu release
using Git.

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

## Related topics

- {doc}`/explanation/ubuntu-linux-kernel-sources`
- <https://wiki.ubuntu.com/Kernel/Dev/KernelGitGuide>

% LINKS

[git package]: https://packages.ubuntu.com/search?keywords=git

% TODO: migrate the rest of the Wiki content
