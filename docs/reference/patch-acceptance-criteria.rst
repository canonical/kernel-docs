.. meta::
   :description: Understand Ubuntu kernel patch acceptance criteria. Learn what patches are accepted for stable releases and the evaluation process used.

.. highlight:: email

.. _ubuntu-patches-acceptance-criteria:

Patch acceptance criteria
=========================

Generally, any patch is eligible for inclusion in the Ubuntu kernel, though some
criteria apply.

Patch category
--------------

A patch falls into 3 categories:

cherry-pick
   The patch is part of the stable upstream for the desired kernel version, but
   picking it with the stable upstream patches may be delayed and there’s a
   request to have the specific patch as soon as possible.

backport
   The patch is upstream (either mainline_ or stable_), but part of a newer
   kernel version, and the submitter asks for a backport to an older Ubuntu
   kernel version.

SAUCE
    The patch is not upstream and/or never will.

Usually, cherry-picks have the biggest rate of approval if it’s done correctly.
Backports and SAUCE patches are a bit tricky. In general, we avoid merging
those as much as possible.

For a detailed description on how to format patches before submission, see
:doc:`./stable-patch-format`, while here is a quick (and far from complete)
introduction.

All patches
-----------

Reasons why the Ubuntu Kernel Team won't approve a patch:

Patch does not apply
^^^^^^^^^^^^^^^^^^^^

The patch should always be based on a recent kernel. Expect to resubmit
again if the tip changes and the patch has conflicts.

SRU patches
-----------

This section describes additional reasons why the Ubuntu Kernel Team won't
approve a SRU patch.

Launchpad bug
^^^^^^^^^^^^^

Each patch must be related to a dedicated Launchpad bug. The bug should be
targeted to the kernels and series that the patch is aiming to lend.

The bug description must follow the `SRU template`_.

.. _SRU template: https://documentation.ubuntu.com/sru/en/latest/reference/bug-template/

See `this example Launchpad bug`_.

.. _this example Launchpad bug: https://bugs.launchpad.net/ubuntu/+source/linux/+bug/1995957


BugLink
^^^^^^^

Patches and cover letter should have a link to a Launchpad bug as the first
line of the description.

The link must be in the short form ``https://bugs.launchpad.net/bugs/XXXXXX``.

Example::

    Subject: [SRU][O/N][PATCH v2 0/1] ALSA: hda/realtek: fix mute/micmute LEDs for a HP EliteBook 645 G10

    BugLink: https://bugs.launchpad.net/bugs/2087983

    ...

The link must not be in its long form
``https://bugs.launchpad.net/ubuntu/+source/linux/+bug/XXXXXX``.

*Bad* example::

    Subject: [SRU][O/N][PATCH v2 0/1] ALSA: hda/realtek: fix mute/micmute LEDs for a HP EliteBook 645 G10

    BugLink: https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2087983

    ...

SRU cover letter
^^^^^^^^^^^^^^^^

The patch should come with a *cover letter* that has both a short link to the
SRU bug and a copy of the *SRU Justification* from the bug. It can be generated
using the ``--cover-letter`` option of the :manpage:`git-send-email(1)` command.

Example cover letter::

    Subject: [SRU][O/N][PATCH v2 0/1] ALSA: hda/realtek: fix mute/micmute LEDs for a HP EliteBook 645 G10

    BugLink: https://bugs.launchpad.net/bugs/2087983

    SRU Justification:

    [ Impact ]

    Mute/mic LEDs don't function on HP EliteBook 645 G10.

    [ Test Plan ]

    Test mute and mic LEDs with proposed kernel once patched.

    [ Where problems could occur ]

    Unknown regressions in the sound subsystem.

    Kernel Engineer (1):
      ALSA: hda/realtek: fix mute/micmute LEDs for a HP EliteBook 645 G10

     sound/pci/hda/patch_realtek.c | 1 +
     1 file changed, 1 insertion(+)

If the patchset is a new version of a previous patchset posted on the
mailing-list, the cover letter should explain what has changed for this new
submission.

If the patchset involved some decisions that were not obvious, it should be
explained in the cover letter to ease the review of the patchset. If you choose
to send a SAUCE patch instead of the other options, the rationale should be
explained in the cover letter.

Cherry-pick or backport
-----------------------

This section describes additional reasons why the Ubuntu Kernel Team won't
approve a cherry-pick or backport patch.

Upstream
^^^^^^^^

The patch should be in the mainline_ or the stable_ tree. Having the patch in
a maintainer subtree is not enough, because the subtree might change. Having
the patch in linux-next_ is bare minimum.

.. _mainline: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/
.. _stable: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/
.. _linux-next: https://www.kernel.org/doc/man-pages/linux-next.html

Source
^^^^^^

.. highlight:: text

The patches should have a *cherry picked from* or *backported from* line with
the appropriate :spellexception:`SHA` from the upstream. It can be generated using the
``-x`` option of the :manpage:`git-cherry-pick(1)` command.
This line should appear just before your *Signed-off-by* line.

.. code-block:: text

   (cherry picked from commit 622f21994506e1dac7b8e4e362c8951426e032c5)

.. code-block:: text

   (backported from commit 622f21994506e1dac7b8e4e362c8951426e032c5)

In case the upstream source is linux-next, you should explicit state it.

.. code-block:: text

   (cherry picked from commit 622f21994506e1dac7b8e4e362c8951426e032c5 linux-next)

In case the upstream source is one of the stable trees, you should indicate
which one the commit belongs to::

     (cherry picked from commit e0aab7b07a9375337847c9d74a5ec044071e01c8 linux-4.19.y)

In case the upstream source is another Ubuntu kernel (even a SAUCE patch), you
can explicit it with the name of the source kernel::

    (cherry picked from commit 622f21994506e1dac7b8e4e362c8951426e032c5 plucky:linux)

In case the provenance is anything else, you should explicit the source git
tree in full::

    (cherry picked from commit 622f21994506e1dac7b8e4e362c8951426e032c5 git://git.kernel.org/pub/scm/linux/kernel/git/broonie/sound.git)

.. highlight:: email

Signed-off-by
^^^^^^^^^^^^^

The patches must have your Signed-off-by (SoB) as the last line, after the
upstream cherry-picked line. It can be generated using the ``-s`` option of the
:manpage:`git-cherry-pick(1)` command.

If the patch is from yourself and already has your SoB, a new SoB must be
added.

Example::

    Subject: [PATCH] ufs: ufs_sb_private_info: remove unused s_{2,3}apb fields

    BugLink: https://bugs.launchpad.net/ubuntu/oracular/+source/linux/+bug/2087853

    These two fields are populated and stored as a "frequently used value"
    in ufs_fill_super, but are not used afterwards in the driver.

    Moreover, one of the shifts triggers UBSAN: shift-out-of-bounds when
    apbshift is 12 because 12 * 3 = 36 and 1 << 36 does not fit in the 32
    bit integer used to store the value.

    Closes: https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2087853
    Signed-off-by: Agathe Porte <agathe.porte@canonical.com>
    Signed-off-by: Al Viro <viro@zeniv.linux.org.uk>
    (cherry picked from commit 6cfe56fbad32c8c5b50e82d9109413566d691569 linux-next)
    Signed-off-by: Agathe Porte <agathe.porte@canonical.com>

.. _mainline: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/
.. _stable: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/
.. _linux-next: https://www.kernel.org/doc/man-pages/linux-next.html

SAUCE
-----

This section describes additional reasons why the Ubuntu Kernel Team won't
approve a SAUCE patch.

SAUCE prefix
^^^^^^^^^^^^

The patches must have the ``UBUNTU: SAUCE:`` prefix.

Example::

    Subject: UBUNTU: SAUCE: wifi: ath11k: avoid deadlock during regulatory update in ath11k_regd_update()

    BugLink: https://bugs.launchpad.net/bugs/1995041

    ...

    Signed-off-by: Aaron Ma <aaron.ma@canonical.com>

Backport or SAUCE
------------------

This section describes additional reasons why the Ubuntu Kernel Team won't
approve a SAUCE or backport patch.

Testing
^^^^^^^

It is very important for patches to have the upstream maintainer(s) review
and do wider testing on different types of hardware for various types of
scenarios. Even though the patch was tested by the submitter, the tests may
be limited to a specific use case and prone to breaking other parts of the
kernel affected by this change. In the case of backports, it was not tested
upstream for the specific kernel version, therefore it may cause issues.

Maintenance
^^^^^^^^^^^

Maintaining a patch in our tree is not easy. Let’s say we include v0.54 of
some patch. Later, we want to sync up to the latest version of this patch.
It’s not easy to simply revert v0.54, because merges could have changed some
of the code. Not to mention, there are very few patches like this that
provide incremental changes between versions.

Core code impact
^^^^^^^^^^^^^^^^

If our kernel contains multiple SAUCE patches or backports, it will diverge
from the upstream kernel. In case we need help from upstream to solve bugs,
we will have to first test if one of these patches does not cause the bug and
then ask the community for help.

Merge conflict
^^^^^^^^^^^^^^

It may cause merge conflicts later when someone from upstream changes the
same piece of code. If the component is prone to frequent changes upstream,
we will have to deal with this a lot and it will require extra effort on our
side.

Security concerns
^^^^^^^^^^^^^^^^^

It may open up unforeseen security issues. Not that this does not happen with
upstream code, but having the code there reaches a wider audience, and more
people are involved in mitigating the issue.

Bug Prone
^^^^^^^^^

It may introduce new bugs that have a wider impact due to limited testing,
especially if the change affects a component used in many places.

Quality
^^^^^^^

Not a very common reason, but the patch may not fit into our standards of
code quality or may not serve any real purpose.

Lack of time
^^^^^^^^^^^^

Maintaining these patches, with all the arguments from above, will be
time-consuming on our side, and we don’t have the resources to both do this
and deliver a stable Linux OS
