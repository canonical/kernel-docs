---
myst:
  html_meta:
    description: "Understand how a kernel patch moves from a bug report through upstream review and into the Ubuntu kernel."
---

# Ubuntu kernel patch life cycle

A patch does not move straight from a developer's tree into the Ubuntu kernel.
It follows a path designed to keep Ubuntu aligned with upstream, maintainable
over the long term, and safe for the wide range of hardware that Ubuntu
supports.

## Overview

The typical life cycle of a patch looks like this:

1. A bug or missing feature is identified.
2. A patch is developed and thoroughly tested.
3. A Launchpad bug is filed to track the issue.
4. The patch is submitted to the upstream Linux kernel.
5. Once accepted upstream, the patch flows down into the Ubuntu kernel.
6. If a patch needs to land in Ubuntu before the next upstream sync, it can be
   cherry-picked or backported through the {doc}`Ubuntu stable release update
   process </explanation/stable-release-updates>`.

This flow reflects a core principle of Ubuntu kernel development: patches that
benefit the whole kernel community should be accepted upstream first. Ubuntu
then consumes those changes through its regular rebasing and update process.

## Why upstream first

The Ubuntu kernel is not a separate fork. It is an Ubuntu packaging and
configuration layer on top of the upstream Linux kernel, plus a small set of
Ubuntu-specific changes. Because of this, the easiest and safest way for a
patch to enter Ubuntu is for it to be accepted into the upstream kernel first.

Submitting upstream has several advantages:

- The patch receives review from the maintainers who know the affected
  subsystem best.
- Wider testing across different hardware and configurations reduces the risk
  of regressions.
- Once the patch is in upstream, it automatically reaches Ubuntu through the
  normal update cycle.

Patches that are not accepted upstream are harder for the Ubuntu kernel team
to carry. They must be maintained across rebases and may conflict with future
upstream changes.

## Tracking work in Launchpad

Every change that lands in an Ubuntu stable kernel is tied to a Launchpad bug.
The bug serves as the record of the problem, the proposed fix, and the
justification for the update.

Before a patch is sent anywhere, the bug description should explain:

- The observable problem or the missing capability.
- The impact on users.
- How the patch resolves the issue.
- How the fix was tested.

The patch can be attached to the bug so reviewers can inspect it, and the bug
number is later referenced in the patch itself through the `BugLink:` line.

## From upstream into Ubuntu

Once a patch is accepted into the upstream Linux kernel or the stable kernel
tree, it will eventually be picked up by Ubuntu through the team's regular
rebase process. The timing depends on which Ubuntu series the patch is needed
for and where it sits in the upstream release cycle.

For patches that need to reach Ubuntu more quickly, the Ubuntu kernel team can
cherry-pick or backport the upstream commit into the relevant Ubuntu kernel
series. This is done through the stable release update process and requires the
patch to meet SRU criteria.

## When a patch is not accepted

A patch may be rejected upstream for many reasons: it may need more testing,
require a different approach, or not fit the upstream direction. When this
happens, the path into Ubuntu becomes much harder.

The Ubuntu kernel team generally does not carry patches that have been
rejected upstream unless there is a strong Ubuntu-specific reason to do so.
In most cases, the correct response is to address the upstream feedback and
resubmit.

## Related topics

- {doc}`/how-to/source-code/send-patches` explains how to send patches to
  the Ubuntu kernel team mailing list.
- {doc}`/reference/patch-acceptance-criteria` describes the criteria for
  accepting patches into the Ubuntu kernel.
- {doc}`/reference/stable-patch-format` covers the required patch format.
- {doc}`/explanation/stable-release-updates` explains how stable release
  updates work.
