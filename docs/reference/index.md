---
myst:
  html_meta:
    description: "Reference guides for Ubuntu kernel development processes. Explore kernel variants, patch formats, acceptance criteria, upload rights, and terminology."
---

# Reference

Reference material about Ubuntu kernel development processes, terminology, and
more.

## Kernel patch & contribution guidelines

It's important to follow the Ubuntu kernel patch guidelines so your contributions are accepted into the Ubuntu kernel tree without delays or rejection.
These pages show how to properly format and submit your patches.

```{toctree}
:maxdepth: 1

stable-patch-format
patch-acceptance-criteria
```

## Kernel variants and snaps

Different kernel variants and branches serve different purposes - long-term support, new hardware enablement, or experimental features.
Understanding them helps you choose the right kernel for testing, development, or deployment.

```{toctree}
:maxdepth: 1

ubuntu-kernels
hwe-kernels
oem-kernels
snap-lifecycle
```

## Privileges

Understand the criteria and process to apply for Ubuntu kernel and DKMS package upload rights.

```{toctree}
:maxdepth: 1

kernel-upload-rights
dkms-upload-rights
```

## General

```{toctree}
:maxdepth: 1

glossary
```
