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

### Point of entry / Installation

```{important}
**BJDEAN GAP?:** As noted in the review 1st September the current documentation doesn't have a entry point for new "users of the kernel" as it starts with people who are patching the kernel. The following section {ref}`contributing-and-participation` may be a good option for now.
```

(contributing-and-participation)=
### Contributing and participation

If you want to take part in Ubuntu kernel work, this is the best place to start.
You can begin by understanding the source packages and workflow, then move on to
testing, reporting, and submitting patches.

{doc}`What the Ubuntu kernel sources are </explanation/ubuntu-linux-kernel-sources>` •
{doc}`How a patch reaches the kernel </explanation/ubuntu-kernel-patch-life-cycle>` •
{doc}`Patch acceptance criteria </reference/patch-acceptance-criteria>` •
{doc}`Stable patch format </reference/stable-patch-format>` •
{doc}`Send patches to the mailing list </how-to/source-code/send-patches>` •
{doc}`Glossary </reference/glossary>`


### Kernel development and customization

This domain covers obtaining source, preparing a development environment, and
building or modifying Ubuntu kernels for development and testing.

{doc}`Enable source package repositories </how-to/source-code/enable-source-repositories>` •
{doc}`Obtain kernel source with Git </how-to/source-code/obtain-kernel-source-git>` •
{doc}`Build a kernel </how-to/develop-customise/build-kernel>` •
{doc}`How-to guides </how-to/index>`

### Release lifecycle and maintenance

Ubuntu kernels move through a structured SRU lifecycle with staged testing and
promotion. This section explains how kernels are maintained for stability,
security, and regression control across releases.

{doc}`Kernel lifecycle (SRU) </explanation/kernel-lifecycle-sru>` •
{doc}`Stable release updates </explanation/stable-release-updates>` •
{doc}`Post-release updates </explanation/post-release-updates>` •
{doc}`Kernel release workflow </reference/kernel-workflow-playbook/kernel-release>` •
{doc}`Kernel rollback workflow </reference/kernel-workflow-playbook/kernel-rollback>`

### Kernel variants and selection

Ubuntu provides multiple kernel variants to suit different hardware and
deployment needs (for example generic, HWE, OEM, and snap-based delivery).
Use this section to understand what each variant is for and how to choose.

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

### Publishing, archive and upload rights

This section covers the systems and permissions around getting kernel changes
into Ubuntu: upload rights, archive paths, and the collaboration surfaces used
by the kernel team.

{doc}`Kernel upload rights </reference/kernel-upload-rights>` •
{doc}`DKMS upload rights </reference/dkms-upload-rights>` •
{doc}`Enable source package repositories </how-to/source-code/enable-source-repositories>` •
{doc}`Obtain kernel source with Git </how-to/source-code/obtain-kernel-source-git>` •
{doc}`Send patches to the mailing list </how-to/source-code/send-patches>`


### Quality

The kernel sits at the core of every Ubuntu system, so it is maintained under
processes designed to keep it reliable and to deliver critical updates without
disrupting users. For how this fits into the wider distribution, see
[How Ubuntu is made](https://ubuntu.com/project/docs/how-ubuntu-is-made/).

{doc}`Test pre-release kernels </how-to/testing-verification/test-pre-release-kernels>` •
{doc}`Security and update policy </explanation/post-release-updates>`


### Where Ubuntu kernels are used

Ubuntu kernels are used across desktop, server, IoT, and cloud deployments.
These pages provide broader platform context and deployment-specific framing.

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
