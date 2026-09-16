---
myst:
  html_meta:
    description: "Official Ubuntu kernel documentation. Learn to build, customize, and contribute to Ubuntu kernels. Understand the cadence for stable release updates and HWE kernels."
---

# Ubuntu Kernel documentation

The Ubuntu Linux kernel is the core software enabling applications to interact
with system resources.

The Stable Release Update (SRU) cycle ensures the kernel stays current, secure,
and stable. Ubuntu-specific configuration, patches, packaging, testing, and
release processes distinguish it from the upstream kernel.

This documentation serves developers, partners, and others working with Ubuntu
kernels - offering guidance on kernel workflows, tools, SRU timelines, and
processes for customization and maintenance.


(in-this-documentation)=
## In this documentation

% DOMAINS OF CONCERN

````{domain}
```{slice} Building
{doc}`About source packages </explanation/ubuntu-linux-kernel-sources>`
{doc}`Enable source repositories </how-to/source-code/enable-source-repositories>`
{doc}`Get the source-code </how-to/source-code/obtain-kernel-source-git>`
{doc}`Build a kernel </how-to/develop-customise/build-kernel>`
{doc}`Build a snap </how-to/develop-customise/build-kernel-snap>`
{doc}`Build a module </how-to/develop-customise/build-kernel-module>`
```

```{slice} Patching
{doc}`Patch life-cycle </explanation/ubuntu-kernel-patch-life-cycle>`
{doc}`Patch format </reference/stable-patch-format>`
{doc}`Patch acceptance </reference/patch-acceptance-criteria>`
{doc}`Sending patches to Ubuntu </how-to/source-code/send-patches>`
```

```{slice} Releasing
{doc}`Stable Release Update (SRU) cycle </explanation/kernel-lifecycle-sru>`
{doc}`Snap lifecycle </reference/snap-lifecycle>`
{doc}`Releasing a kernel </reference/kernel-workflow-playbook/kernel-release>`
```

```{slice} Variants
{doc}`Kernel variants </reference/ubuntu-kernels>`
{doc}`HWE </reference/hwe-kernels>`
{doc}`OEM </reference/oem-kernels>`
```

```{slice} Kernel quality
{doc}`About the SRU </explanation/stable-release-updates>`
{doc}`Post-release updates </explanation/post-release-updates>`
{doc}`Testing pre-release </how-to/testing-verification/test-pre-release-kernels>`
{doc}`Rollback </reference/kernel-workflow-playbook/kernel-rollback>`
```

```{slice} Contributing
{doc}`Upload rights </reference/kernel-upload-rights>`
{doc}`DKMS upload rights </reference/dkms-upload-rights>`
{doc}`Documentation </how-to/contribute>`
```
````

```{important}
**TODO: "Upstream" slice (after Variants):** In [kernel-docs PR#119](https://github.com/canonical/kernel-docs/pull/119) we have incoming documentation on how to send patches upstream
```


## How this documentation is organized

This documentation uses the [Diátaxis documentation structure](https://diataxis.fr/).

* {doc}`/how-to/index` assumes you have basic familiarity with kernel development and provide generic instructions for common tasks involved in kernel development.
* {doc}`/reference/index` provides detailed information about submitting patches and their criteria, and other processes related to Ubuntu kernels.
* {doc}`explanation/index` discusses the different aspects of the Ubuntu kernel and kernel development process at Canonical.


## Project and community

Kernel documentation is a member of the Ubuntu family. It’s an open source
documentation project that warmly welcomes community contributions, suggestions,
fixes and constructive feedback.

* [Code of conduct](https://ubuntu.com/community/docs/ethos/code-of-conduct)
* [Contribute to kernel docs](/how-to/contribute)

```{toctree}
:hidden:
:maxdepth: 2

/how-to/index
/reference/index
/explanation/index
```
