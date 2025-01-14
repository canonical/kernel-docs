.. _kernel-upload-rights:

Kernel upload rights
####################

Those who are allowed to upload the kernel to the Ubuntu archive have a serious
responsibility.

To obtain per package upload rights for the Ubuntu kernel, you need to apply to
become a member of the ubuntu-kernel-uploaders_ team in Launchpad. People can
join this team only after going through a thorough application and review
process.

The sections below describe the general member profile of the
ubuntu-kernel-uploaders_ team, as well as the application process.

Member profile
==============

Below is the general profile for those having per package upload rights for the
Ubuntu kernel.

- Generally have commit access to the `Ubuntu kernel git repositories`_.

- Actively follow and participate in discussions and patch reviews on the
  `Ubuntu kernel-team mailing list`_.

- Are collectively responsible for the maintenance of packages in the Ubuntu
  kernel package set for all supported releases as well as the development
  release.

- Have a strong working knowledge of kernel packaging concepts and techniques,
  refined through experience.

- Have a strong working knowledge of Ubuntu project procedures, especially
  those related to the release process and support commitments, and an
  understanding of the reasons why they exist.

- Have a history of substantial and direct contribution to the distribution,
  particularly to kernel-related packages.

- Feel a sense of personal responsibility for the quality of Ubuntu releases
  and for the satisfaction of Ubuntu users.

- Exercise great care in their work, with the understanding that their efforts
  have a direct impact on others, including:

  - every Ubuntu user;
  - the Ubuntu release team;
  - corporate partners who provide support for Ubuntu.

Application process
===================

As alluded to in the member profile above, membership consideration for the
ubuntu-kernel-uploaders_ team adheres to a strict policy. Anyone considering
applying should align with the general profile outlined in the previous section
and meet the criteria listed below:

1. A thorough understanding of the Ubuntu kernel patch submission process:

   a. Demonstrates an understanding of this process by having submitted
      multiple patches which were accepted over a six-month development cycle.

   b. Demonstrates an understanding of this process by having reviewed and
      Ack'd/Nack'd multiple patches over a six-month development cycle.

2. A thorough understanding of the Ubuntu release cycle and associated
   milestone and freeze dates.

3. A thorough understanding of the Ubuntu Kernel :ref:`sru-cycle-cadence`.

4. A thorough understanding of the upstream kernel development cycle and how it
   relates to the Ubuntu kernel development cycle.

5. Demonstrate a chain of trust by having multiple sponsored kernel uploads
   over a six-month development cycle by various existing members of the
   ubuntu-kernel-uploaders team.

If you are not an official ubuntu-kernel-uploaders member yet, but fulfill all
of the criteria above, you are likely a promising candidate for joining the
team.

Application template
--------------------

If you are interested in joining, start by preparing your application using the
following template:

https://wiki.ubuntu.com/Kernel/Dev/PPUApplicationTemplate

An example application can also be seen at the following: 

https://wiki.ubuntu.com/LuisHenriques/PerPackageUploaderApplication 

At least three existing ubuntu-kernel-uploaders members must confirm that they
have worked with you sufficiently to assess your skills and verify that you meet
the criteria above. These three individuals are typically your sponsors.

Screening process
=================

Once your application has been prepared and you are ready to be screened,
send an email to the `Ubuntu kernel-team mailing list`_ requesting your
application be reviewed.

You will then get a notification from the team about the scheduled IRC meeting
(#ubuntu-kernel channel at irc.libera.chat) where you will be interviewed and a
vote regarding your membership will be taken. 

As part of the interview you will be asked to briefly introduce yourself, so
prepare a 2-3 line introduction beforehand to speed up the process. Only
existing members of the ubuntu-kernel-uploaders team are allowed to vote. An
applicant must receive a minimum of 3 Ack's in order to be added to the team. 

Once an applicant has successfully passed the application process, an
announcement will be made to both the Ubuntu kernel-team and `devel-permissions
mailing lists`_. The applicant will then be added to the
ubuntu-kernel-uploaders team by an administrator.

.. _devel-permissions mailing lists: https://lists.ubuntu.com/mailman/listinfo/devel-permissions
.. _ubuntu-kernel-uploaders: https://launchpad.net/~ubuntu-kernel-uploaders
.. _Ubuntu kernel git repositories: http://kernel.ubuntu.com/git
.. _Ubuntu kernel-team mailing list: https://lists.ubuntu.com/mailman/listinfo/kernel-team
