---
myst:
  html_meta:
    description: "Guide to obtain Ubuntu kernel source code from the Ubuntu archive."
---

```{owners} team:ckt-tnt
```

# How to obtain source for an Ubuntu kernel release from the archive

This guide covers a few ways to get a source tarball for an Ubuntu kernel.
If you want a complete git tree please see the guide on [obtaining source via
git](/how-to/source-code/obtain-kernel-source-git).

## Downloading the latest source tarball

If you need the latest source tarball, the standard way to obtain it is via
`apt-get source`. To use `apt-get source` you first need to [enable a `deb-src`
repository](/how-to/source-code/enable-source-repositories) in your apt
configuration. Once that's done, you can get a source tarball for your kernel
with this command:

```shell
apt-get source linux-headers-$(uname -r)
```

## Downloading a specific version of the source

For older versions that may not be available via apt, you can get the
tarball from Launchpad using `pull-lp-source`. This command comes from the
`ubuntu-dev-tools` package, so you may need to install that first.

```shell
apt install ubuntu-dev-tools
```

Then, you can get source for your *currently installed* version of the kernel
using this command:

```shell
pull-lp-source linux-headers-$(uname -r)
```

This is expected to take a while longer than via apt.

## Downloading unreleased versions

For versions which have not yet been published to the archive,
you'll need to access the in-development source tree [via
git](/how-to/source-code/obtain-kernel-source-git).
