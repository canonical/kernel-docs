# Ubuntu Kernel Variants and Branches

Ubuntu maintains several kernel variants to balance the needs of stability, hardware enablement, and rapid development. This document outlines the primary kernel trees, their roles in the development lifecycle, and the git branching strategies used by the Canonical Kernel Team.

For detailed technical references, please consult the {doc}`../index` and [Ubuntu kernels from Canonical](<https://ubuntu.com/kernel>).

## Ubuntu Development Kernels

Ubuntu releases every 6 months; therefore, the Canonical Kernel Team constantly works on the active Ubuntu development series to integrate the latest Linux kernel features for the release. The development kernels serve as the testing ground for new features, upstream updates, and partner integration before they reach the stable releases.

### The ``linux-unstable`` Tree

The [linux-unstable tree](<https://code.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/unstable>) represents the bleeding edge of Ubuntu kernel development. It is a fast-moving target designed to track the latest upstream Linux developments.

* **Upstream Alignment:** It is usually rebased weekly against the latest upstream Release Candidate (``-rcX``) during the most active development period. New patches are also constantly applied to the branch.
* **Volatility:** Patchsets can be removed if problems are found.
* **Purpose:** It serves as the initial landing ground for upstream code and feature integration. It may still lack support for core components (e.g., AppArmor, NVIDIA drivers, ZFS, etc.); therefore, it is not guaranteed to have all features necessary to fully support an Ubuntu system.
* **Availability:** As it usually does not have all core components necessary to run a full Ubuntu user-space, it is available only via development PPAs and not in the Ubuntu archive.

### The ``linux`` Tree

Once a ``linux-unstable`` kernel version includes support for all core components and is deemed relatively stable, it is moved to the ``linux`` tree.

* **Upstream Alignment:** Similar to the ``linux-unstable`` tree, it usually follows the latest upstream release. However, rebases are less frequent as some level of stability needs to be maintained. During a development cycle, it is expected to be updated to all ``major.minor`` upstream releases until the last version available before the Ubuntu release GA.
* **Purpose:** The ``linux`` kernel is the Ubuntu generic kernel which will be available as the default choice for most installations, and will be the base for all derivatives and custom kernels based on the same upstream ``major.minor`` version.

### Ubuntu Kernel Next (UKN)

Because the ``linux-unstable`` kernel moves too fast for larger integration work, the Canonical Kernel Team maintains the [Ubuntu Kernel Next](<https://canonical-kteam-docs.readthedocs-hosted.com/public/reference/kernels/uknext/uknext.html>) tree, which is an integration tree designed to bridge the gap between the volatility of ``linux-unstable`` and the stability required for partner development.

* **Workflow:** It is a periodic, read-only snapshot of ``linux-unstable``.
* **Integration:** It provides a stable codebase for integration work into the next development kernel. Integration issues (e.g., conflicts) can be spotted and fixed earlier.

## Optimized Kernels

In addition to the generic kernel, Canonical also provides optimized kernels which are derived from the generic kernel. For more information please consult [Ubuntu kernel variants from Canonical](<https://ubuntu.com/kernel/variants>).

* **Purpose:** Kernels that have their configuration, hardware support, or additional features optimized for a variety of hardware platforms and workloads. Examples include kernels optimized for the Raspberry Pi ARM board (``linux-raspi``), for running as guests on the major public cloud providers, for IoT devices, etc.
* **Release and update cadence:** Optimized kernels are released and receive security updates with the same cadence as the Ubuntu generic kernel upon which they are based.

### OEM Kernels

OEM kernels are optimized derivatives designed specifically for Original Equipment Manufacturer (OEM) projects to support hardware pre-installed with Ubuntu. For more information please consult {doc}`oem-kernels`.

* **Purpose:** They address unique timelines and hardware needs that may not align with the generic kernel release cadence and scope.
* **Staging Strategy:** OEM kernels often serve as a staging area. Modifications made here are intended to be merged into the generic Ubuntu kernel in subsequent releases.

## Production and Enablement Kernels

Once an Ubuntu version is released (General Availability), all kernels available in that release become production-ready and stable. They are maintained for the duration of the Ubuntu release support period and receive security updates and bug fixes via {doc}`Stable Release Updates (SRU) <../explanation/stable-release-updates>`.

### HWE (Hardware Enablement) Kernels

Hardware Enablement (HWE) kernels are available for Ubuntu Long Term Support (LTS) releases. They provide a way for LTS users to consume newer kernel versions and receive support for newer hardware (such as the graphics stack). For more information please consult {doc}`hwe-kernels`.

* **Rolling Release:** HWE kernels are "rolling" in nature; they are typically backported from subsequent interim or LTS Ubuntu releases to the previous LTS.
* **Lifecycle:** HWE kernels are supported until the next HWE stack is released, at which point users are encouraged to upgrade to the newer version.

## Git Branching Strategy

When working with Ubuntu kernel repositories, you will primarily interact with two key branches.

### ``master`` branch

The ``master`` branch represents the current state of the kernel source as it exists in the ``-updates`` pocket of the Ubuntu archive. It contains the linear history of all the stable releases published for that kernel.

### ``master-next`` branch

The ``master-next`` branch serves as the staging area for the **next** Stable Release Update (SRU).

* **Purpose:** Commits intended for the next update are applied here first after being reviewed and acknowledged by the Canonical Kernel Team. This branch will also contain commits for the kernel builds that are published for testing in the ``-proposed`` pocket of the Ubuntu archive.
* **Flow:** Patches land in ``master-next`` for integration and testing before being promoted to ``master`` after the kernel SRU update is published to ``-updates``.
