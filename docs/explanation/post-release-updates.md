# Kernel security and update policy for post-release trees

This document describes the process and criteria for post-release kernel updates.

The kernel is a very complex source package, and it is fundamentally different than other packages in the archive.
The described process and criteria are built on the normal {doc}`Stable release updates </explanation/stable-release-updates>` document, and where these documents conflict, this document takes precedence.

## What sort of updates are allowed for post-release kernels?

In addition to the generic {term}`SRU` requirements, the Ubuntu Kernel team will accept patches that fall into any of the following categories:

1. It fixes a critical issue (e.g. data-loss, OOPs, crashes) or is security related.
   Security related issues might be covered by security releases which are special in handling and publication.
1. Simple, obvious and short fixes or hardware enablement patches.
   If there is a related upstream stable tree open, this class of patches is required to come through the upstream process.
   Patches sent upstream for that reason must include their BugLink reference.
1. The patch is included in a corresponding upstream stable or extended stable release.
   For the lifetime of both LTS and non-LTS release, the Ubuntu Kernel team will be pulling upstream stable updates from the corresponding series.
   There will be one tracking bug report for each stable update but additional references to existing bugs will be added to the contained patches (on a best-effort basis).
4. Fixes to drivers which are not upstream are accepted directly if they fall into the first two categories.

## How does the process work?

- First step for every SRU is to have a bug associated with the patch.

- The patch or patchset must contain the link to the Launchpad bug and contain a "Signed-off-by" line from the submitter.
  See {doc}`/reference/stable-patch-format` for detailed requirements on the Ubuntu Kernel SRU patch format.

- The beginning of the description area of the bug needs to have a SRU justification which should look like this example:

  ```text
  SRU Justification:
  Impact: <a short description about the symptoms and the impact of the bug>
  Fix: <how was this fixed, where did the fix come from>
  Testcase: <how can the fix be tested>
  ```

- If the fix for a problem meets the requirements for SRU and has been tested to successfully solve the bug, then the next step depends on whether the fix is serious enough to be directly applied to an Ubuntu kernel series and/or
  whether it should go in via upstream stable (as long as that is appropriate
  for upstream stable).

  - For fixes for serious issues, the patch should be sent to the [kernel-team mailing list] in parallel to being submitted upstream.
    SRU patches submitted for inclusion into an Ubuntu kernel require ACK's from at least two senior Ubuntu Kernel team members before being applied to an Ubuntu kernel tree.
    Again, even when going into an Ubuntu kernel tree on an accelerated path, the patch should also be submitted upstream.
    See the {ref}`Stable patch format example <ref-stable-patch-format-series-example>` for more information.

  - For all other patches that do not need an accelerated path into an Ubuntu kernel, it is advised to push the fix upstream when appropriate (i.e. the problem also exists upstream) and CC [stable@kernel.org] during the process.
    As soon as the patch is accepted into upstream/upstream-stable, it will find it's way back down into our Ubuntu kernel in a subsequent release.
    This ensures patches are getting vetted and applied upstream, which reduces overall maintenance costs for the Ubuntu Kernel team.

## How will updates be provided in the archive?

- Security updates will be uploaded directly into -security without other changes.
  The next full release will include these security changes in addition to the normal changes.

- Normal updates will be provided as pre-releases through the corresponding kernel build PPA.
  At certain points those get made into proposed releases which are uploaded to the -proposed pocket.
  Before proposed releases can migrate to other pockets, it must be verified that the changes fix the targeted issues without causing regressions.

% LINKS

[kernel-team mailing list]: mailto:kernel-team@lists.ubuntu.com
[stable@kernel.org]: mailto:stable@kernel.org