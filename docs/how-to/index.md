---
myst:
  html_meta:
    description: "Guides for Ubuntu kernel development. Learn how to obtain source code, build kernels, test in -proposed versions, and contribute to the documentation."
---

# How-to guides

These guides accompany through the various stages and building and publishing
kernel packages and components.

```{toctree}
:titlesonly:
:maxdepth: 1
:hidden:

Source code access and management </how-to/source-code/index>
Development and customization </how-to/develop-customise/index>
Test kernels in -proposed </how-to/testing-verification/test-kernel-in-proposed>
Contribute to kernel docs </how-to/contribute>
Kernel Bisect </how-to/kernel-bisection>
```

## Source code access and management

Get access to kernel source code if you need to modify the kernel for specific
requirements, optimize the performance for selected hardware, inspect the source
tree to build custom kernel modules, and more.

- [Obtain kernel source for an Ubuntu release using Git](/how-to/source-code/obtain-kernel-source-git)

## Development and customization

The steps to build a kernel is similar but may have slightly difference
configuration requirements on different platforms and/or architectures.

- [Build an Ubuntu Linux kernel](/how-to/develop-customise/build-kernel)
- [Build an Ubuntu Linux kernel snap](/how-to/develop-customise/build-kernel-snap)

## Testing and verification

These guides relate to testing the kernel to ensure its stability and
functionality before you push or release a patch.

- [Test kernels in -proposed](/how-to/testing-verification/test-kernel-in-proposed)

## Debug and Troubleshooting

These guides explain how to debug and troubleshoot a kernel bug should you
encounter one.

- [Kernel Bisect](/how-to/kernel-bisection)
