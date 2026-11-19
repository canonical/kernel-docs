.. meta::
   :description: DKMS (Dynamic Kernel Module Support) upload rights for Ubuntu. Understand permissions, responsibilities, and application procedures.

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

See for example this request for the mofed-modules-24.10 package:

.. code-block:: none

   Subject: Request to add mofed-modules-* to kernel-dkms packageset
   From: agathe.porte@canonical.com
   Date: Tue Jan 7 13:25:09 UTC 2025
   To: devel-permissions@lists.ubuntu.com
    
   Hello,
    
   I recently introduced the following packages in the archive:
    
   - mofed-modules-24.07: https://launchpad.net/ubuntu/+source/mofed-modules-24.07
   - mofed-modules-24.10: https://launchpad.net/ubuntu/+source/mofed-modules-24.10
   
   To ease the upload process and not rely on coredevs or MOTU for upload,
   we need to add them to the kernel-dkms packageset:
   
   - mofed-modules-24.07 for oracular
   - mofed-modules-24.10 for plucky and oracular [2]
   
   FYI, I may apply to get PPU to this kernel-dkms packageset in the
   future. It would make more sense for me for the kernel team owners to
   review the application but since there are no kteam admins I guess this
   needs to go through the DMB.
   
   Thanks.
   
   Agathe.
   
   [1] eg. for oracular:
       https://ubuntu-archive-team.ubuntu.com/packagesets/oracular/kernel-dkms
   
   [2] Note that the mofed-modules-24.10 package has been sitting in the
       NEW queue for oracular for more than a month, but we would need the
       upload rights on this one too. If you have any tips on how I can get
       attention for this package to enter oracular, they are welcome.

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
