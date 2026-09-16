---
myst:
  html_meta:
    description: "Official Ubuntu kernel documentation. Learn to build, customize, and contribute to Ubuntu kernels. Understand the cadence for stable release updates and HWE kernels."
---

# Ubuntu Kernel documentation

The Ubuntu Linux kernel is the core software enabling applications on Ubuntu to
interact with system resources.

The Ubuntu kernel handles communication between system hardware and user-space
applications, managing tasks like memory, processing, and security. Regular
stable release updates (SRU) ensure the kernel stays secure, stable, and
optimized.

Ubuntu kernels provide a reliable foundation for applications and system
processes, meeting the need for secure, high-performance, Ubuntu environments.
Kernels are also tested consistently for regressions to provide users with a
reliable and smooth experience. Kernels are tailor made for Ubuntu Desktop,
Ubuntu Server, a wide range of architectures, IoT devices, cloud providers, and
more.

This documentation serves developers, partners, and others working with Ubuntu
kernels, offering guidance on kernel workflows, tools, SRU timelines, and
processes for customization and maintenance.


(in-this-documentation)=
## In this documentation

% DOMAINS OF CONCERN

```{list-table}
:widths: 30 70
:header-rows: 0

* - **About the Kernel**
  - {doc}`About the source-code </explanation/ubuntu-linux-kernel-sources>`

* - **Building**
  - {doc}`Enable source repositories </how-to/source-code/enable-source-repositories>`
    • {doc}`Get the source-code </how-to/source-code/obtain-kernel-source-git>`
    • {doc}`Build a kernel </how-to/develop-customise/build-kernel>`
    • {doc}`Build a snap </how-to/develop-customise/build-kernel-snap>`
    • {doc}`Build a module </how-to/develop-customise/build-kernel-module>`

* - **Patching**
  - {doc}`Patch life-cycle </explanation/ubuntu-kernel-patch-life-cycle>`
    • {doc}`Patch format </reference/stable-patch-format>`
    • {doc}`Patch acceptance </reference/patch-acceptance-criteria>`
    • {doc}`Sending patches to Ubuntu </how-to/source-code/send-patches>`

* - **Releasing**
  - {doc}`Stable Release Update (SRU) cycle </explanation/kernel-lifecycle-sru>`
    • {doc}`Snap lifecycle </reference/snap-lifecycle>`
    • {doc}`Releasing a kernel </reference/kernel-workflow-playbook/kernel-release>`

* - **Variants**
  - {doc}`Kernel variants </reference/ubuntu-kernels>`
    • {doc}`HWE </reference/hwe-kernels>`
    • {doc}`OEM </reference/oem-kernels>`

* - **Upstream**
  - TODO: In [kernel-docs PR#119](https://github.com/canonical/kernel-docs/pull/119) we have incoming documentation on how to send patches upstream

* - **Kernel quality**
  - {doc}`About the SRU </explanation/stable-release-updates>`
    • {doc}`Post-release updates </explanation/post-release-updates>`
    • {doc}`Testing pre-release </how-to/testing-verification/test-pre-release-kernels>`
    • {doc}`Rollback </reference/kernel-workflow-playbook/kernel-rollback>`

* - **Contributing**
  - {doc}`Upload rights </reference/kernel-upload-rights>`
    • {doc}`DKMS upload rights </reference/dkms-upload-rights>`
    • {doc}`Documentation </how-to/contribute>`
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
