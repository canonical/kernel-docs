---
myst:
  html_meta:
    description: "Why Ubuntu offers unmodified upstream mainline kernel builds, why they are unsupported, and how they coexist with Ubuntu kernels on your system."
---

```{owners} team:ckt-tnt
```

(exp-mainline-builds)=
# About mainline kernel builds

## What mainline builds are, and why they exist

By default, Ubuntu systems run the Ubuntu kernels from the Ubuntu repositories. Those kernels carry Ubuntu's patches. It's useful to be able to test with an unmodified upstream kernel for two reasons:

- To locate problems that come from Ubuntu's kernel patches.
- To confirm that upstream has fixed a specific issue.

Mainline builds make this practical. They're built from unmodified kernel source, using the Ubuntu kernel configuration files, and packaged as Ubuntu `.deb` files. This saves you the time of compiling a kernel and debugging build issues yourself.

The Ubuntu kernel isn't bit-for-bit the same as the mainline kernel. A mainline build is a comparison point, not a replacement.

To run a test, see {doc}`/how-to/testing-verification/test-with-mainline-kernel`. For archive details, see {doc}`/reference/mainline-builds`.

## Support and security

Mainline builds are produced for debugging, so they come with no support. They aren't appropriate for production use.

They also receive no security updates. If you install one manually, you never receive a security update or patch for that version. This is why the how-to guide asks you to remove the kernel when you finish testing.

This is also why verification matters. Few things compromise the security of a Linux system worse than a compromised kernel. Every published file is checksummed, and the checksums file is signed with the mainline builder's key. Verifying confirms two things:

- The packages were built by the Ubuntu mainline build system.
- The packages are bit-for-bit identical to the files on the server.

## How mainline kernels fit on your system

### They install alongside Ubuntu kernels

Mainline kernels have their own ABI namespace. Each kernel gets a separate directory under `/lib/modules/<version>`, so mainline and Ubuntu kernels can be installed at the same time. You choose between them from the GRUB boot menu.

This is why testing doesn't replace your normal kernel. It's also why removing a mainline kernel afterwards is a choice rather than a requirement for booting normally.

### Out-of-tree modules often break

Mainline kernels are built with the toolchain from either the most recent Ubuntu stable release or the development release. Out-of-tree modules that you built for your release kernel are therefore unlikely to work with a mainline build. The exception is when your release is also the release that supplies the toolchain. For an LTS release, that's true for only part of the cycle.

Modules that are rebuilt at install time, such as DKMS modules, can fail to build against the new kernel. For this reason, the how-to guide asks you to remove them first.

### They can't be used from a live session

You can use a mainline kernel in two ways:

- Install it on an installed system, restart, and choose it at boot.
- Build a live environment that contains the new kernel.

The second takes considerable effort, so testing from an installed system is the practical choice.

## Related topics

- {doc}`/how-to/testing-verification/test-with-mainline-kernel`
- {doc}`/reference/mainline-builds`
- {doc}`/reference/ubuntu-kernels`