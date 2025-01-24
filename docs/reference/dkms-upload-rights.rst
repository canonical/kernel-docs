DKMS upload rights
##################

Sometimes you want to be able to upload the DKMS package without having get full
MOTU_ or `Ubuntu Core Developer`_ rights. The *kernel-dkms packageset* is a
list of packages that can be uploaded by members of the
ubuntu-kernel-dkms-uploaders_ Launchpad team.

There is one packageset per release. See for example the 
`Noble kernel-dkms packageset`_.

.. _Noble kernel-dkms packageset: https://ubuntu-archive-team.ubuntu.com/packagesets/noble/kernel-dkms
.. _ubuntu-kernel-dkms-uploaders: https://launchpad.net/~ubuntu-kernel-dkms-uploaders
.. _MOTU: https://wiki.ubuntu.com/UbuntuDevelopers#MOTU
.. _Ubuntu Core Developer: https://wiki.ubuntu.com/UbuntuDevelopers#CoreDev

Adding packages to the packageset
=================================

If you need to add DKMS packages to the packageset, send a mail to the
``devel-permissions@lists.u.c`` mailing list. List the source
packages and releases you need in your request.

See for example `this request for the mofed-modules-24.10 package`_.

.. _this request for the mofed-modules-24.10 package: https://lists.ubuntu.com/archives/devel-permissions/2025-January/002679.html

Applying for packageset upload rights
=====================================

Like all applications, you first need to create a wiki page with your
application details. Use the DeveloperApplicationTemplate_ to create your
``DKMSUploadApplication`` page. See for example
`PaoloPisati/DKMSUploadApplication`_.

.. _PaoloPisati/DKMSUploadApplication: https://wiki.ubuntu.com/PaoloPisati/DKMSUploadApplication
.. _DeveloperApplicationTemplate: https://wiki.ubuntu.com/UbuntuDevelopment/DeveloperApplicationTemplate

Then, you will need to reserve a meeting with the `Developer Membership Board
(DMB)`_ for applying [#]_. To do so, `edit the DMB agenda`_ to add yourself to a
free slot.

.. [#] Unlike the ubuntu-kernel-uploaders_ Launchpad group for
   :ref:`kernel-upload-rights`, the kernel team `has no admin`_ for the
   ubuntu-kernel-dkms-uploaders_ Launchpad group. This means we have no team
   process to review applications and must delegate to the DMB.

.. _edit the DMB agenda: https://wiki.ubuntu.com/DeveloperMembershipBoard/Agenda
.. _ubuntu-kernel-uploaders: https://launchpad.net/~ubuntu-kernel-uploaders
.. _has no admin: https://launchpad.net/~ubuntu-kernel-dkms-uploaders/+contactuser
.. _Developer Membership Board (DMB): https://wiki.ubuntu.com/DeveloperMembershipBoard
