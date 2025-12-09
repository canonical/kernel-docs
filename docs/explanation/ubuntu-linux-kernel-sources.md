# About Ubuntu Linux kernel sources

Ubuntu Linux kernel source packages are essential for users and developers who
want to build, modify, or understand the kernel that powers Ubuntu systems.
These packages are stored in Launchpad and organized by series (or release),
making it easy to find and work with the appropriate kernel version for any
given Ubuntu release.

## Launchpad Git URL structure for Ubuntu kernel sources

The Launchpad Git repository URL for Ubuntu Linux kernel sources follow one of
the general formats below:

```{code-block} text
https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/<source>/+git/<series>
https://git.launchpad.net/~canonical-kernel/ubuntu/+source/<source>/+git/<series>
```

For example, the source for the generic Jammy Jellyfish (Ubuntu 22.04 LTS)
can be found at:

```{code-block} text
https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy
```

While the URL for the AWS kernel variant for Noble Numbat (Ubuntu 24.04 LTS) is:

```{code-block} text
https://git.launchpad.net/~canonical-kernel/ubuntu/+source/linux-aws/+git/noble
```

You can get the correct URL by checking the list of Git repositories for
the [Ubuntu Kernel Repositories team] or [Canonical Kernel team], or in the
automatically updated list of [currently supported Ubuntu kernel Repositories].

## Kernel source repository branches

You will find the following branches in each Ubuntu kernel source repository.

- `master`: The source for the Ubuntu {spellexception}`distro` kernel.
- `master-next`: Contains the commits that will be merged into the `master`
  branch for the next stable release update (SRU) for the series.

(exp-ubuntu-kernel-source-protocols)=

## Protocols for accessing kernel sources

| Protocol | Authentication needed? | Use case | Command sample |
| -------- | ---------------------- | -------- | -------------- |
| Git protocol   | No               | Public repositories, require read-only access   | `git clone git://<kernel source URL>`     |
| SSH protocol   | Yes (SSH key)    | Private repositories, require write access      | `git clone git+ssh://<kernel source URL>` |
| HTTPS protocol | Yes (if private) | Public and private repositories,for easy access | `git clone https://<kernel source URL>`   |


% LINKS

[Ubuntu Kernel Repositories team]: https://code.launchpad.net/~ubuntu-kernel/+git
[Canonical Kernel team]: https://code.launchpad.net/~canonical-kernel/+git
[currently supported Ubuntu kernel Repositories]: https://kernel.ubuntu.com/git/
