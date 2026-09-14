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
  - {doc}`/explanation/ubuntu-linux-kernel-sources`

* - **Building the Kernel**
  - {doc}`/how-to/source-code/enable-source-repositories` • {doc}`/how-to/source-code/obtain-kernel-source-git` • {doc}`/how-to/develop-customise/build-kernel` • {doc}`/how-to/develop-customise/build-kernel-snap` • {doc}`/how-to/develop-customise/build-kernel-module`

* - **Patching the Kernel**
  - {doc}`/explanation/ubuntu-kernel-patch-life-cycle` • {doc}`/reference/stable-patch-format` • {doc}`/reference/patch-acceptance-criteria` • {doc}`/how-to/source-code/send-patches`

* - **Releasing the Kernel**
  - {doc}`/explanation/kernel-lifecycle-sru` • {doc}`/reference/snap-lifecycle` • {doc}`/reference/kernel-workflow-playbook/kernel-release`

* - **Kernel Variants**
  - {doc}`/reference/ubuntu-kernels` • {doc}`/reference/hwe-kernels` • {doc}`/reference/oem-kernels`

* - **Linux: The Upstream Kernel**
  - TODO: In [kernel-docs PR#119](https://github.com/canonical/kernel-docs/pull/119) we have incoming documentation on how to send patches upstream

* - **A Stable and Reliable Kernel**
  - {doc}`/explanation/stable-release-updates` • {doc}`/explanation/post-release-updates` • {doc}`/how-to/testing-verification/test-pre-release-kernels` • {doc}`/reference/kernel-workflow-playbook/kernel-rollback`

* - **Contributing to the Ubuntu Kernel**
  - {doc}`/reference/kernel-upload-rights` • {doc}`/reference/dkms-upload-rights` • {doc}`/how-to/contribute`
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
