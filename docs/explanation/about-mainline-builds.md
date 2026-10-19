---
myst:
  html_meta:
    description: "Explains what Ubuntu mainline kernel builds are and how they help distinguish upstream issues from Ubuntu kernel changes."
---

```{owners} team:ckt-tnt
```

(exp-mainline-builds)=

# About mainline kernel builds

The Ubuntu Kernel Team publishes builds from upstream kernel source, using
Ubuntu kernel configuration files and packaging the result as `.deb` files.
These mainline builds let you compare an issue with upstream kernel code.

Ubuntu kernels include Ubuntu-specific patches and configuration, so they
differ from mainline builds. Comparing the two can help determine whether an
issue is specific to Ubuntu's changes or is also present upstream. A mainline
build is a diagnostic comparison, not a replacement for an Ubuntu kernel.

## Module compatibility

Differences in the kernel interface and {spellexception}`toolchain` used to
build kernels mean that modules built for an Ubuntu kernel might not work with
a mainline build.

To compare kernels in a bug investigation, see
{doc}`/how-to/testing-verification/test-with-mainline-kernel`. For the
mainline archive structure, see {doc}`/reference/mainline-builds`.