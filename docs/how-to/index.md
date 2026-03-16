---
myst:
  html_meta:
    description: "Guides for Ubuntu kernel development. Learn how to obtain source code, build kernels, test in -proposed versions, and contribute to the documentation."
---

# How-to guides

These guides accompany through the various stages of building and publishing
kernel packages and components.

```{toctree}
:titlesonly:
:maxdepth: 1
:hidden:

Enable kernel source package repositories </how-to/source-code/enable-source-repositories>
Obtain kernel source for an Ubuntu release using Git </how-to/source-code/obtain-kernel-source-git>
Send patches to the mailing-list </how-to/source-code/send-patches>
Build an Ubuntu Linux kernel </how-to/develop-customise/build-kernel>
Build an Ubuntu Linux kernel snap </how-to/develop-customise/build-kernel-snap>
Test kernels in -proposed </how-to/testing-verification/test-kernel-in-proposed>
Contribute to kernel docs </how-to/contribute>
```

## Source code access and management

You can get access to kernel source code via `apt` or directly from the kernel Git repositories.
You can also check the formatting requirements, review process, and best practices for submitting kernel patches to the Ubuntu kernel team mailing list.

- {doc}`Enable kernel source package repositories </how-to/source-code/enable-source-repositories>`
- {doc}`Obtain kernel source for an Ubuntu release using Git </how-to/source-code/obtain-kernel-source-git>`
- {doc}`Send patches to the mailing-list </how-to/source-code/send-patches>`

## Development and customization

The steps to build a kernel is similar but may have slightly difference configuration requirements on depending on the build package (snap, debs), platform and/or architectures.

- {doc}`Build an Ubuntu Linux kernel </how-to/develop-customise/build-kernel>`
- {doc}`Build an Ubuntu Linux kernel snap </how-to/develop-customise/build-kernel-snap>`

## Testing and verification

These guides relate to testing the kernel to ensure its stability and
functionality before you push or release a patch.

- [Test kernels in -proposed](/how-to/testing-verification/test-kernel-in-proposed)
