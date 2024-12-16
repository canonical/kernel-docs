# About kernel stable release updates (SRU)

Every supported kernel for an Ubuntu release is part of a Stable Release Updates
(SRU) cycle. The Ubuntu Kernel {term}`SRU` is a structured procedure to ensure
that kernel updates in Ubuntu's stable releases are both reliable and
non-disruptive to users.

This document aims to provide an overview about the various aspects of the
Ubuntu kernel SRU process.

## SRU purpose

Kernel SRU focuses on delivering necessary updates without changing core
functionalities with low potential of introducing regressions in stable Ubuntu
releases. This typically covers:

- Upstream stable updates
- Bug fixes that address relevant issues or improve system stability
- Common Vulnerabilities and Exposures (CVE) security updates
- Hardware enablement (HWE) patches

## SRU cycle cadence

Since August 2023, the Ubuntu Kernel team has adopted a 4/2 Kernel SRU cycle to
improve predictability and responsiveness. It involves a 4-week ("4/") stable
update cycle for regular fixes and features, combined with an additional
mid-cycle 2-week ("/2") update focused on urgent CVE security patches and
critical fixes. This approach enables more timely updates for critical issues
while maintaining stability, and continues to support mid-cycle
{ref}`respins <exp-sru-kernel-respins>` for regression fixes as needed.

```{figure} /_images/exp-kernel-sru-life cycle-stages.svg
:alt: Ubuntu kernel life cycle stages and ideal SRU 4/2 cadence timeline

Ubuntu kernel life cycle stages and ideal SRU 4/2 cadence timeline
```

See the [Ubuntu Kernel Team] home page for details on SRU cycle dates.

```{important}
While the Ubuntu kernel team strives to meet the SRU cycle 4/2 cadence, please
note that SRU cycle dates are tentative. As such, they cannot be guaranteed and
may be subject to change.
```

## SRU patch submission and review process

All updates that are applied to stable kernels go through the following patch
submission and review process. More details can be found at [Ubuntu Wiki -
Stable Patch Format].

### Patch creation

The first step for every SRU is to create a patch containing all the necessary
information, including a link to the associated public Launchpad bug report that
contains the SRU justification.
The only exception to this are CVE fixes, where only the CVE number is required.

See the [Ubuntu Wiki - Kernel Updates] for more information on the SRU
requirements and justification.

### Patch submission

Next, contributors send the stable patches to the Ubuntu Kernel Team mailing
list (kernel-team@lists.ubuntu.com) for review.
Where appropriate, the patch should also be submitted to upstream stable in
parallel.

### Mailing list review

Stable patch sets on the mailing list (ML) are then carefully reviewed by the
Ubuntu Kernel Team.
This review process involves validating that the patch fixes the intended
issues, ensuring no regressions are introduced to the kernel, evaluating the
risk and relevance of including the patch into a stable release, and
reconciling mainline and Ubuntu-specific changes.

### Patch acceptance

Once a mailing list patch has been vetted and has at least two `ACK`s from
senior members of the Ubuntu Kernel Team, the commit will then be applied to the
associated stable Ubuntu kernel tree.
The patch will then be considered for release in an upcoming SRU cycle if all
the patch acceptance criteria are met.

See the {doc}`Ubuntu patch acceptance criteria </reference/patch-acceptance-criteria>`
for more information.

(exp-sru-kernel-respins)=
## SRU kernel respins

A respin is a rebuild of a kernel package replacing a previous build. During
each SRU cycle, kernel respins may need to happen for several reasons.

- A regression was introduced in a previous cycle or in the current cycle.
- Additional fixes need to be added.
- An important update needs to be added mid-cycle which cannot wait until the
next cycle.

## Kernel streams

Kernels that are ready for the full suite of testing and verification are
promoted to the "testing" phase, where the built kernel binaries (and artifacts)
are copied to a proposed location.

As the [Ubuntu archive has a single proposed pocket], the support for multiple
kernel streams was implemented in the kernel SRU workflow.
These streams consist of a set of locations (Ubuntu archive pockets or PPAs)
that can be used for parallel (and generally independent) preparation and
testing of kernels.

For example, when a respin is required for a regression released in the previous
cycle it can be prepared while the kernel spin for the current SRU cycle is
still in progress. These streams are also what enables the 4/2 Kernel SRU cycle
model.

## Related topics

- [Discourse - Ubuntu Kernel 4/2 SRU Cycle Announcement]
- [Ubuntu Wiki - Stable Kernel Release Cadence]
- [Kernel team stable dashboard]

% LINKS

[Ubuntu Kernel Team]: https://kernel.ubuntu.com/
[Ubuntu Wiki - Stable Patch Format]: https://wiki.ubuntu.com/Kernel/Dev/StablePatchFormat
[Ubuntu Wiki - Kernel Updates]: https://wiki.ubuntu.com/KernelTeam/KernelUpdates
[Ubuntu archive has a single proposed pocket]: https://canonical-ubuntu-packaging-guide.readthedocs-hosted.com/en/latest/explanation/archive/#archivepockets
[Discourse - Ubuntu Kernel 4/2 SRU Cycle Announcement]: https://discourse.ubuntu.com/t/ubuntu-kernel-4-2-sru-cycle-announcement/37478
[Ubuntu Wiki - Stable Kernel Release Cadence]: https://wiki.ubuntu.com/Kernel/StableReleaseCadence
[Kernel team stable dashboard]: https://kernel.ubuntu.com/reports/kernel-stable-board/
