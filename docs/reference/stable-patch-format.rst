Stable patch format
===================

Every Ubuntu LTS release during standard security maintenance period welcomes
contributions from anyone.
However, patches must comply with the required format.

See `The Ubuntu lifecycle and release cadence`_ for more information.

Prerequisites
-------------

Subscribe `here
<https://lists.ubuntu.com/mailman/listinfo/kernel-team>`__ to join
kernel-team@lists.ubuntu.com before submitting your first patch. Messages
from non-subscribers will be held in a queue pending admin approval.

Preparing commits
-----------------

Every patch **must** adhere to the following guidelines.

Subject line
^^^^^^^^^^^^

Every patch submitted to a stable kernel **must** have have its subject line
starting with "[SRU]" followed by the release name against which the
patch is targeted.

The release name **must** be enclosed in "[ ]" brackets and **should** be
abbreviated using the first letter of the release name (e.g. "N" for
"Noble"). For example:

.. code-block:: none

   [SRU][N][PATCH 0/1] Fix error of resume on rtl8168fp

* If a patch is to be applied to multiple releases, a list of release names
  must be provided. For example, when it targets Bionic and Focal:

  .. code-block:: none

     [SRU][B/F][PATCH 1/1] KVM: fix overflow of zero page refcount with ksm running

  .. note::

     Historically, the rule has been somewhat flexible, and various styles
     have been permitted. You may find examples like the following in the
     `mailing list archive
     <https://lists.ubuntu.com/archives/kernel-team/>`__:

     .. code-block:: none

        [SRU][B,F][PATCH 1/1] KVM: fix overflow of zero page refcount with ksm running
        or
        [SRU][B][F][PATCH 1/1] KVM: fix overflow of zero page refcount with ksm running
        or
        [SRU][Bionic,Focal][PATCH 1/1] KVM: fix overflow of zero page refcount with ksm running
        or
        [SRU][Bionic/Focal][PATCH 1/1] KVM: fix overflow of zero page refcount with ksm running
        or
        [SRU][Bionic][Focal][PATCH 1/1] KVM: fix overflow of zero page refcount with ksm running

     Please adhere to the ``[B/F]`` style.

     * Use initial letter(s) in UPPER case
     * Separate each series with "/"

* If the patch has to be applied to a specific derivative for multiple
  releases, indicate the derivative after the release. For example:

  .. code-block:: none

     [SRU][B:linux-kvm/F:linux-kvm] [PATCH 0/1] UBUNTU: [Config] kvm: Add support for modifying LDT

Subject line for non-upstream patches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   Upstream patches refer to patches that only include commits that already
   reside in Linus's mainline tree.

If the patch requested doesn't come from upstream, it must contain one of the
following on the subject line after the release name and patch number.

.. list-table::
   :header-rows: 1

   * - Descriptor
     - Meaning
   * - UBUNTU\: SAUCE\:
     - This is a patch to the kernel code that has not been applied on mainline
       (Linus' tree). This category covers the following cases:

       #. The submitter has either authored the patch or obtained the patch from
          a non-upstream source.
       #. The patch has been applied to an upstream tree but not yet merged on
          mainline.
       #. The patch is never expected to be submitted upstream but is of enough
          value for Ubuntu to carry it in our tree.
       #. The patch has been submitted to upstream but is of enough value for
          Ubuntu to carry it in our tree regardless of upstream acceptance.

   * - UBUNTU: [Packaging]
     - This is an update relevant to Ubuntu Packaging, including the contents
       of the various ``debian*/`` directories.
   * - UBUNTU: [Config]
     - This is an update to the kernel configuration as recorded in the
       ``debian.<branch>/config`` directory. 

       See the ``debian.master/config/README.rst`` :none:`wokeignore:rule=master,`
       or `Discourse - Kernel configuration in Ubuntu`_ for more information
       about the config format.
   * - UBUNTU: ubuntu
     - This is an update to an Ubuntu specific driver in the ``ubuntu/``
       directory. This category is rarely used anymore except in special cases.
   * - UBUNTU:
     - This subject line is internally used by some automation scripts.
       Avoid using it unless none of the other categories are appropriate for
       your patch.

For example, for a patch that falls under the "UBUNTU: SAUCE:" category:

.. code-block:: none

   [SRU][F][PATCH 2/2] UBUNTU: SAUCE: shiftfs: prevent ESTALE for LOOKUP_JUMP lookups


Comment body
^^^^^^^^^^^^

#. Every patch associated with a Launchpad bug must have a link to the bug in
   the commit's comment section in the form of a "BugLink" block.

   A "BugLink" block must immediately follow the subject line and be the first
   text in the body of the commit comment. A "BugLink" block consists of:

   #. A blank line.
   #. One or more lines containing "BugLink:" and a URL to the Launchpad bug.
      The URL must be of the format:
      "https\://bugs.launchpad.net/bugs/<bug-id>", where <bug-id> is the
      bug number of the associated Launchpad bug tracker.
   #. Another blank line.

   Every stable patch **must** have an associated Launchpad bug for
   tracking by the kernel stable and SRU teams. Exceptions are patches for
   CVE fixes (:ref:`see below <comment-body-cve>`).

   Example:

   .. code-block:: none
      :emphasize-lines: 2-4

      Subject: [SRU][F][PATCH 1/1] UBUNTU: SAUCE: netfilter: nf_tables: Fix EBUSY on deleting unreferenced chain

      BugLink: https://bugs.launchpad.net/bugs/2089699

      [...]

#. Every patch **must** have a "Signed-off-by" line for the person submitting
   the patch. The "Signed-off-by" line **must** follow all other provenance
   lines and should be the last line in the commit comment.

   Example:

   .. code-block:: none
      :emphasize-lines: 4

      Signed-off-by: Jesse Barnes <jbarnes@virtuousgeek.org>
      Signed-off-by: Linus Torvalds <torvalds@linux-foundation.org>
      (backported from commit 5620ae29f1eabe655f44335231b580a78c8364ea)
      Signed-off-by: Manoj Iyer <manoj.iyer@canonical.com>

#. Every patch **must** display the provenance of the patch. We want to
   preserve where the patch came from, who signed off on it, who ack'd it,
   whether it was cherry-picked from upstream and applied cleanly or not and
   who finally applied it to an official Ubuntu source tree.

   Backported patches:

   - If the patch required changes (e.g. it did not apply cleanly), use
     "backported from commit <sha1>" between brackets "()". For example:

     .. code-block:: none

        (backported from commit <sha1> <upstream repo name>)

     There must be a brief explanation immediately after the "(backported from
     ...)" block, between square brackets, with the name of the person who
     introduced the change.

     .. code-block:: none

        (backported from commit <sha1> <upstream repo name>)
        [roxanan: Had to adjust the context due to missing commit <sha1>]

   Cherry-picked patches:

   - If the patch is a simple cherry-pick from an upstream repo and it applies
     cleanly, that **must** also be spelled out in the provenance section in the
     format "backported from commit <sha1>" between brackets "()". For example:

     .. code-block:: none

        (cherry picked from commit <sha1> <upstream repo name>)

     .. note::

        Omit the "<upstream repo name>" if the patch comes from the mainline tree.

   Example:

   .. code-block:: none
      :emphasize-lines: 4

      Signed-off-by: Adam Jackson <ajax@redhat.com>
      Signed-off-by: Eric Anholt <eric@anholt.net>
      Signed-off-by: Greg Kroah-Hartman <gregkh@suse.de>
      (cherry picked from commit d4e0018e3e4dd685af25d300fd26a0d5a984482e linux-2.6.34.y)
      Signed-off-by: Manoj Iyer <manoj.iyer@canonical.com>

   .. _comment-body-cve:
#. Every **CVE** patch **must** contain a line at the beginning of the commit
   message that specifies the CVE number(s) related to the patch. This must be
   the first part of the body of the comment.

   There is the comment subject line, a blank line, the CVE number, a blank
   line, and then the rest of the comment body.
   A "BugLink" is optional for CVE patches.

   Example:

   .. code-block:: none
      :emphasize-lines: 5-11

      Subject: [SRU][B/D] UBUNTU: SAUCE: nbd_genl_status: null check for nla_nest_start

      From: Navid Emamdoost <navid.emamdoost@gmail.com>

      CVE-2019-16089

      nla_nest_start may fail and return NULL. The check is inserted, and
      errno is selected based on other call sites within the same source code.
      Update: removed extra new line.
      v3 Update: added release reply, thanks to Michal Kubecek for pointing
      out.
      [...]


Preparing to submit patches
---------------------------

In most cases, patches should be submitted as a patch series accompanied by
a cover letter. However, if the patch series is relatively large (e.g. more
than 20 commits), consider sending a git pull request instead.

Sending as a patch series
^^^^^^^^^^^^^^^^^^^^^^^^^

#. Every patch submitted to a stable kernel **must** be sent in a patch series
   with a cover letter, even if the patch series contains a single patch.

#. The cover letter **must** contain the "BugLink" or the CVE number like the
   patch(es) itself.

#. The cover letter **must** contain the SRU justification from the launchpad
   bug or the CVE fix.
   See `KernelTeam/KernelUpdates`_ wiki for more information about the SRU
   justification format to be added to a bug.

#. All the emails in the patch series **must** be numbered (e.g. "[PATCH 0/3]",
   "[PATCH 1/3]", etc.) and all the patches sent in reply to the cover letter
   (PATCH 0/N).

   .. tip::

      When sending patches with git-send-email, use the option
      "\-\-suppress-cc=all" in order to prevent adding the original author of
      the patch and other people from the provenance block as CC.

Sending as a pull request
^^^^^^^^^^^^^^^^^^^^^^^^^

#. Include the git pull request information in the cover letter email.

#. The cover letter **must** contain the "BugLink" or the CVE number like the
   patch(es) itself.

#. The cover letter **must** contain the SRU justification from the launchpad
   bug or the CVE fix.
   See `KernelTeam/KernelUpdates`_ wiki for more information about the SRU
   justification format to be added to a bug.

#. The subject line of the cover letter **must** contain the "[PULL]" tag,
   instead of "[PATCH X/N]".

#. The git repository **must** be publicly accessible.

#. The body of the commits should follow the same rules as for a patch series.

#. The format of the title of the commits contained in the pull request should
   be the same as for the patch series, except for the tags at the beginning of
   the subject enclosed in "[]" brackets which would be removed by ``git am``
   on application.

Submitting the patch
--------------------

Stable patches must be sent to kernel-team@lists.ubuntu.com.

Once the patch receives two "Acked-by" replies from members of the Ubuntu
Kernel Team, it will be merged.

Patch series example
--------------------

Here is an excerpt from an example patch series that adheres to the guidelines.

Cover letter (PATCH 0/1)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

   Subject: [SRU][F][PATCH 0/1] s390/cpum_cf: Add new extended counters for IBM z15 (LP: 1881096)
   From: frank.heimes@canonical.com
   Date: 24.06.20, 22:11
   To: kernel-team@lists.ubuntu.com

   BugLink: https://bugs.launchpad.net/bugs/1881096

   SRU Justification:

   [Impact]

   With perf from Ubuntu 20.04 on IBM z15 hardware, some counters
   reported with lscpumf are not usable with 'perf stat -e'.
   [...]

   [Fix]

   Cherry-pick upstream commit:
   d68d5d51dc89 ("s390/cpum_cf: Add new extended counters for IBM z15")

   [Test Plan]

   Requires the fix/patch of the perf tool, as mentioned in the bug, too.
   [...]

   [Where problems could occur]

   The regression can be considered as low, since:
   [...]

   [Other Info]

   This requires a patch to be included into the perf itself, too - please
   see bug description for more details.
   [...]

Patch 1/1
^^^^^^^^^

.. code-block:: none

   Subject: [SRU][F][PATCH 1/1] s390/cpum_cf: Add new extended counters for IBM z15
   From: frank.heimes@canonical.com
   Date: 24.06.20, 22:11
   To: kernel-team@lists.ubuntu.com

   From: Thomas Richter <tmricht@linux.ibm.com>

   BugLink: https://bugs.launchpad.net/bugs/1881096

   Add CPU measurement counter facility event description for IBM z15.

   Signed-off-by: Thomas Richter <tmricht@linux.ibm.com>
   Reviewed-by: Sumanth Korikkar <sumanthk@linux.ibm.com>
   Signed-off-by: Vasily Gorbik <gor@linux.ibm.com>
   (cherry picked from commit d68d5d51dc898895b4e15bea52e5668ca9e76180)
   Signed-off-by: Frank Heimes <frank.heimes@canonical.com>

   [...]

Related topics
--------------

* `KernelTeam/KernelUpdates`_:
  shows the SRU Justification format to be added to a bug.
* `ubuntu-check-commit`_:
  script to check commits against Ubuntu submission rules.

.. LINKS

.. _The Ubuntu lifecycle and release cadence: https://ubuntu.com/about/release-cycle
.. _Discourse - Kernel configuration in Ubuntu: https://discourse.ubuntu.com/t/kernel-configuration-in-ubuntu/35857
.. _KernelTeam/KernelUpdates: https://wiki.ubuntu.com/KernelTeam/KernelUpdates
.. _ubuntu-check-commit: https://kernel.ubuntu.com/gitea/actions/ubuntu-check-commit/src/branch/main/ubuntu-check-commit
