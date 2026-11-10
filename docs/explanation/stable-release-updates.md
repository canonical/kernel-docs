---
myst:
  html_meta:
    description: "Understand Ubuntu kernel stable release updates (SRU). Learn about the 2-week unified cycle, weekly releases, patch submission, review process, held kernels, and the -proposed pocket."
---

```{owners} team:ckt-stable
```

```{tags} sru, respin, mailing lists, kernel dashboard
```

# About kernel stable release updates (SRU)

The Ubuntu Kernel Stable Release Updates ({term}`SRU`) is a structured procedure
to ensure that kernel updates in Ubuntu's stable releases are both reliable and 
non-disruptive to users.

Supported Ubuntu kernels proceed through each SRU cycle, though individual
kernels may be held or dropped from a particular cycle based on quality gates, 
testing results, and specific release needs. 

This document aims to provide an overview about the various aspects of the
Ubuntu kernel SRU process.

## SRU purpose

Kernel SRU focuses on delivering necessary updates without changing core
functionalities with low potential of introducing regressions in stable Ubuntu
releases. This is especially critical for addressing the growing volume of
{spellexception}`CVEs` and security vulnerabilities. Typical updates covered
include:

- Upstream stable updates
- Bug fixes that address relevant issues or improve system stability
- Common Vulnerabilities and Exposures (CVE) security updates
- Hardware enablement (HWE) patches

(sru-cycle-cadence)=

## SRU cycle cadence

The Ubuntu Kernel Team has transitioned to a [unified 2-week Stable Release
Update cycle] published weekly. This rapid cycle enables faster delivery of
critical CVE fixes and security updates while maintaining rigorous testing and
certification standards.

The cycles cascade -- each cycle begins the week after the previous one starts,
resulting in kernel releases happening weekly.

- **Week 1 - Preparation (builds, smoke tests, integration and regression
  testing)**

  Kernel package preparation phase where updates and patches are selected for
  each kernel based on specific needs. Builds are created, and smoke tests,
  {spellexception}`distro` integration, and regression testing confirm kernels
  boot and run correctly. By the end of this week, kernels are published in
  the `-proposed` pocket for early testing by users.

- **Week 2 - Certification testing**

  Extensive certification testing through the
  [Ubuntu Certified](https://ubuntu.com/certified) program. Kernels are
  rigorously tested on different hardware types to ensure reliability and
  stability. By the end of this week, test artifacts are completed.

- **Release**

  Kernels that pass our tests and quality standards are released to the
  `-updates` and `-security` pockets and are ready for production.

Individual kernels may be held, deferred, or excluded from a particular cycle
depending on testing results, quality gates, or specific release needs.

```{figure} /_images/kernel-2-week-sru.png
:alt: Ubuntu kernel SRU cycle timeline

Ubuntu kernel SRU cycle timeline
```

See the [Ubuntu Kernel Team] home page for details on SRU cycle dates.

## SRU patch submission and review process

All updates that are applied to stable kernels go through the following patch
submission and review process. More details can be found at
{doc}`/reference/stable-patch-format`.

### Kernel access

The Ubuntu Kernel Team maintains [kernel repositories for collaborative
development](https://kernel.ubuntu.com/git/).

If you are a Canonical partners or customers, reach out to a member of the
Ubuntu Kernel Team for other means of collaboration.

### Patch creation

The first step for every SRU is to create a patch containing all the necessary
information, including a link to the associated public Launchpad bug report that
contains the SRU justification.
The only exception to this are CVE fixes, where only the CVE number is required.

See the {doc}`ubuntu-project-docs:SRU/reference/exception-Kernel-Updates` for
more information on the Kernel SRU requirements and justification.

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

See the {doc}`/reference/patch-acceptance-criteria`
for more information.

(exp-sru-kernel-held)=

## Held kernels

Given the overlapping 2-week SRU cadence, there is limited flexibility to
respin kernels without impacting subsequent release cycles. As a result,
kernels may need to be held or deferred from a release cycle for various
reasons, including:

- A regression was introduced in the current cycle.
- Additional critical fixes need to be added before release.
- Quality assurance or certification testing failed or has not yet completed.
- Specific release needs require excluding a kernel from a particular cycle.

Once held kernels are resolved and meet all quality criteria, they proceed to
release in a subsequent cycle.

## Kernel streams

Kernels progress through a testing and release pipeline as part of the SRU
cycle. The `-proposed` pocket is key to this process.

- **-proposed pocket:**

  During Week 1 of the SRU cycle, kernel release candidates are published in the
  `-proposed` pocket for early testing by users and systems that prioritize
  faster turnaround over waiting for certification. This allows users to begin
  their own acceptance tests and catch issues before full release. Kernels in
  `-proposed` are updated weekly as part of the overlapping SRU cycles.

- **Certified and released kernels:**

  After passing Week 2 certification and extensive testing, kernels are released
  to the `-updates` and `-security` pockets.

  Individual kernels may be held, deferred, or excluded from a particular cycle
  based on testing results and quality gates, so not every kernel proceeds
  through every cycle.

## Related topics

- [Kernel team stable dashboard]

% LINKS

[Ubuntu Kernel Team]: https://kernel.ubuntu.com/
[unified 2-week Stable Release Update cycle]: https://canonical.com/blog/accelerating-delivery-of-cve-fixes-with-a-new-kernel-release-strategy
[Kernel team stable dashboard]: https://kernel.ubuntu.com/reports/kernel-stable-board/
