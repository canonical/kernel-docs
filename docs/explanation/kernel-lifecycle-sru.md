---
myst:
  html_meta:
    description: "Ubuntu kernel terminology glossary. Find definitions for SRU, DKMS, HWE, edge kernels, and other kernel development terms. Quick reference guide."
---

# Ubuntu kernel SRU lifecycle

Each Stable Release Update (SRU) cycle, kernels move through several stages
from initial preparation and build testing through to final publication in the
``-updates`` or ``-security`` pockets. Each stage adds more testing and
confidence before the kernel reaches a broader audience.

## Preparation

The lifecycle begins when the kernel sources are prepared and cranked, uploading
packages to the build PPA. The goal is to confirm that package generation is
proceeding correctly. The kernel is not yet ready for testing at this point.

## Build PPA and early testing

Once built, the kernel undergoes early validation in the build PPA:

- **boot-testing**: confirms the kernel boots
- **abi-testing**: checks ABI compatibility
- **sru-review**: review by the kernel SRU team
- **new-review**: review by the Archive Admin team

A kernel at this stage is a candidate only. It has not been signed with
official Canonical keys and has not yet undergone broad testing.

## Promote to -proposed

Once early testing and reviews pass, the kernel is copied to ``-proposed``,
passing through a signing PPA first if it contains artifacts that require
signing. At this point the kernel is fully formed and all signed elements carry
official Canonical keys.

## Testing in -proposed

With the kernel in ``-proposed``, formal testing begins:

- **automated-testing**: Ubuntu Auto Package Testing (ADT)
- **certification-testing**: testing on certified platforms in the
  certification team's lab
- **regression-testing**: CKCT testing in the kernel team lab
- **verification-testing**: validation of individual bugs that have an original
  report in Launchpad

{spellexception}`Signoffs` are also collected here — from the security team, the kernel owner,
and where needed, the kernel team internally.

This is the main confidence-building phase. The kernel stays in ``-proposed``
until all required tests and {spellexception}`signoffs` are complete.

## Promote to -updates and -security

Once testing is complete and the cycle is ready to release, the kernel is
promoted to ``-updates`` and is considered ready for general use. If the
security team's signoff indicates it is required, the kernel is also released
to ``-security``.
