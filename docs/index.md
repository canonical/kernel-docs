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
:widths: 25 75
:header-rows: 0

* - **Contributing to Ubuntu kernels**
  - {doc}`/reference/patch-acceptance-criteria` • {doc}`/reference/stable-patch-format` • {doc}`/how-to/source-code/send-patches` • {doc}`/how-to/source-code/send-patches-upstream`
* - **Kernel development**
  - {doc}`/how-to/source-code/enable-source-repositories` • {doc}`/how-to/source-code/obtain-kernel-source-git` • {doc}`/how-to/develop-customise/build-kernel` • {doc}`/how-to/develop-customise/build-kernel-snap` • {doc}`/how-to/testing-verification/test-pre-release-kernels` • {doc}`/explanation/ubuntu-linux-kernel-sources`
* - **Kernel release and maintenance**
  - {doc}`/explanation/kernel-lifecycle-sru` • {doc}`/reference/kernel-workflow-playbook/kernel-release` • {doc}`/reference/kernel-workflow-playbook/kernel-rollback`
* - **Kernel variants**
  - {doc}`/explanation/stable-release-updates` • {doc}`/explanation/post-release-updates` • {doc}`/reference/hwe-kernels` • {doc}`/reference/oem-kernels` • {doc}`/reference/ubuntu-kernels/`
* - **Upload rights**
  - {doc}`/reference/kernel-upload-rights` • {doc}`/reference/dkms-upload-rights`
```

### Getting started

If you would like to understand how an Ubuntu kernel is put together, where
it comes from, and how you might take part — whether by reporting and testing
as a user, or by sending patches:

{doc}`What the Ubuntu kernel sources are </explanation/ubuntu-linux-kernel-sources>` •
{doc}`How a patch reaches the kernel </explanation/ubuntu-kernel-patch-life-cycle>` •
See above {ref}`Contributing to Ubuntu kernels above <in-this-documentation>` •
{doc}`Glossary </reference/glossary>`

```{important}
**BJDEAN GAP:** nothing here answers "how can I participate?" directly.

The patch life cycle page starts further along than a newcomer does. A short "How you can take part" explanation belongs at the head of this section and is likely part of new-content to be added or imported from the old wiki.
```

### What Ubuntu kernels offer

If you're deciding which kernel suits your hardware, release or deployment it's important to know that Ubuntu ships more than one kernel. For an overview of our kernels a good place to start is [Ubuntu kernels from Canonical](https://ubuntu.com/kernel) and [Ubuntu kernel variants from Canonical](https://ubuntu.com/kernel/variants).

Further information available in this document:

{doc}`Variants and branches </reference/ubuntu-kernels>` •
{doc}`HWE kernels </reference/hwe-kernels>` •
{doc}`OEM kernels </reference/oem-kernels>` •
{doc}`Kernel snap lifecycle </reference/snap-lifecycle>`

```{important}
**BJDEAN GAP:** these pages answer "how" but not "why" or "what".

For example the HWE page assumes the reader already knows what hardware
enablement is and why they would want it; compare the plain-language answer at
https://askubuntu.com/questions/248914/what-is-hardware-enablement-hwe

A short HWE explanation, and the framing used on ubuntu.com/kernel, would
make this section work as an entry point rather than a filing shelf.
Note some of this information is in the glossary but could be more prominent.
```

### Resources

```{important}
**BJDEAN TODO:** is this section useful / needed?
```

For readers who need to reach the systems around the kernel: the archive,
Launchpad, and the kernel team mailing list.

{doc}`Enable source package repositories </how-to/source-code/enable-source-repositories>` •
{doc}`Obtain kernel source with Git </how-to/source-code/obtain-kernel-source-git>` •
{doc}`Send patches to the mailing list </how-to/source-code/send-patches>`

% GAP: no single page names Launchpad, the build PPAs, the -proposed pocket and
% the mailing list as a set, so several how-tos re-explain them in passing.

### Quality

The kernel is part of the Ubuntu project - see [How Ubuntu is made](https://ubuntu.com/project/docs/how-ubuntu-is-made/). As the kernel is very complex and at the core of any Ubuntu system processes exist to ensure the kernel is reliable and that critical updates are applied while being non-disruptive to users:

{doc}`/explanation/kernel-lifecycle-sru` • {doc}`/explanation/post-release-updates` • {doc}`/explanation/stable-release-updates`


### Lifecycle

Each Stable Release Update (SRU) cycle, kernels move through several stages
from initial preparation and build testing through to final publication in the
-updates or -security pockets. Each stage adds more testing and confidence
before the kernel reaches a broader audience.

For more information see {doc}`/explanation/kernel-lifecycle-sru`.


### Where Ubuntu kernels are used

The Ubuntu kernel is at the heart of all Ubuntu distributions - for more information see:

[The Ubuntu Linux kernel](https://ubuntu.com/kernel) •
[Ubuntu for the Internet of Things](https://ubuntu.com/internet-of-things) •
[Ubuntu on public clouds](https://ubuntu.com/cloud/public-cloud)


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
