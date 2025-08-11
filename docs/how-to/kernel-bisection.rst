Introduction
============

If you are reading this because you were referred here to bisect your
kernel, or you want to know more about kernel bisecting, then you are
taking the best route to get your bug resolved as soon as possible. This
article is written with the intention that any one at any skill level
may go from start to finish successfully, working through each section
one at a time. If you get stuck, please feel free to ask for
`help <https://ubuntu.com/support/community-support>`__.

What is a bisect?
=================

A bisect (sometimes called a forward bisect), is the fastest process of
finding the midpoint between a known good software version release, and
a known bad one released afterwards. One continues finding the
successive midpoint until one identifies the last good software version
release, followed consecutively by the first bad one.

Performing a bisect is faster than testing every version in between the
initial known good version, and the known bad one. For example, if your
known good release was 1.0, and bad was 1.10, the worst case scenario is
testing 9 releases (1.1, 1.2, 1.3,..., 1.9) until 1.9 was found to be
the last known good version. However, bisecting the worst case scenario,
one would test only 4 releases (1.5, 1.7, 1.8, and 1.9).

What is a reverse bisect?
=========================

A reverse bisect is the process of finding the midpoint between a known
bad software version release, and a known good one released afterwards.
One continues finding the successive midpoint until one identifies the
last bad software version release, followed consecutively in version by
the first good one.

How do I bisect a Ubuntu kernel bug?
====================================

For example, you started with a fully updated Xenial Xerus 16.04 install
using kernel 4.4 and you had no problem. Then, instead of upgrading you
just did a clean install of Bionic Beaver 18.04, and found what appears
to be a `linux <https://launchpad.net/ubuntu/+source/linux>`__ kernel
bug. Hence, to confirm this is a regression in the linux kernel, to rule
out a userspace issue, and to identify the specific regression, the next
step is release bisecting Ubuntu.

Release bisecting Ubuntu
------------------------

Hence, one typically wants to narrow down the first Ubuntu release after
Xenial this problem began in. So, we have the following releases:

+------------------------------+
| Ubuntu 18.04 Bionic Beaver   |
|                              |
| Ubuntu 17.10 Artful Aardvark |
|                              |
| Ubuntu 16.04 Xenial Xerus    |
+------------------------------+

The midpoint release between Xenial and Bionic is Ubuntu 17.10 Artful
Aardvark. One may download releases from
http://releases.ubuntu.com/. If the bug is reproducible in
Artful, then one would want to test Bionic. If this is reproducible in
Bionic, then one knows that the regression happened going from Xenial to
Artful. The next step is version bisecting Ubuntu kernels.

Version bisecting Ubuntu kernels
--------------------------------

Continuing the prior example, the next step is to find the last good
kernel version, followed consecutively in version by the first bad one.
So, assuming the Xenial kernel was kept updated, as per
https://launchpad.net/ubuntu/xenial/+source/linux, the last
Xenial kernel version published for upgrade as of May 19, 2018 was
4.4.0-125.150. As one may notice under the **Releases in Ubuntu**
section, a series of kernels are listed vertically:

+---------------+
| 4.4.0-123.147 |
|               |
| 4.4.0-124.148 |
|               |
| 4.4.0-125.150 |
+---------------+

.. tip::
   Please note one may utilize the same link with a different
   release name to bisect other Ubuntu kernels:

   https://launchpad.net/ubuntu/bionic/+source/linux

   https://launchpad.net/ubuntu/artful/+source/linux

Next, assuming the kernel bug was found in the most recent kernel
version released for Artful, one will click "`View
changelog <https://launchpad.net/ubuntu/artful/+source/linux/+changelog>`__"
and as of May 19, 2108 this is 4.13.0-42.47.

Since we know 4.4.0-125.150 came before 4.13.0-42.47, the next step is
to install kernel 4.13.0-17.20 (the midpoint between the first release
of Artful and the most recent). Consulting
https://launchpad.net/ubuntu/+source/linux/4.13.0-17.20, one will
click **amd64**. Once at the build
`page <https://launchpad.net/~canonical-kernel-team/+archive/ubuntu/ppa/+build/13684017>`__
one will see under:

+----------------------------------+
| **Built files**                  |
|                                  |
| Files resulting from this build: |
+----------------------------------+

-  the following files to install:

+-----------------------------------------------------------------------+
| linux-headers-4.13.0-17-generic_4.13.0-17.20_amd64.deb (685.9 KiB)    |
|                                                                       |
| linux-headers-4.13.0-17_4.13.0-17.20_all.deb (10.4 MiB)               |
|                                                                       |
| linux-image-4.13.0-17-generic_4.13.0-17.20_amd64.deb (19.9 MiB)       |
|                                                                       |
| linux-image-extra-4.13.0-17-generic_4.13.0-17.20_amd64.deb (30.1 MiB) |
+-----------------------------------------------------------------------+

.. warning::
   Please note the files to install above is not an
   exhaustive list. You may need to install more dependencies on what you are
   bisecting.

Instructions on installing kernels may be found at
`here <https://wiki.ubuntu.com/Kernel/MainlineBuilds>`__. If the bug is
reproducible, one now knows that the Ubuntu kernel bug was introduced
between 4.13.0-17.20 and 4.13.0-42.47. The next step is commit bisecting
Ubuntu kernels.

Commit bisecting Ubuntu kernels
-------------------------------

What do I need to build and commit bisect Ubuntu kernels?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The rest of this page assumes that you know how to fetch a kernel from
the Ubuntu git repository, build it, and bisect it. If you can't do that
yet, try starting with `this wiki
page <https://wiki.ubuntu.com/Kernel/BuildYourOwnKernel>`__. As well,
one may want to familiarize themselves with git bisect via a terminal:

.. code:: shell

   git bisect --help

Example of commit bisecting Ubuntu kernels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The commands in the example on this page use a real life example. In
January of 2011, a kernel which was published to the -proposed pocket
caused Radeon graphics to break for a number of users. Typing the
commands as shown on this page will recreate the steps taken to find the
bad commit in that release. The entire history of testing the bisected
kernels for that regression `appears in the
bug <https://bugs.launchpad.net/ubuntu/+source/linux/+bug/703553>`__.

Getting set up
^^^^^^^^^^^^^^

You need to have a bug reproducer, or have a cooperative tester in the
community. If you can't reliably determine whether the bug exists in a
given kernel, bisection will not give meaningful results.

This process goes a lot faster if you can quickly build kernels and have
them tested. Using a fast build machine and having good communications
with the testers will speed things up.

Check out your tree and get ready
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to follow along with the example, use the commands exactly
as shown:

.. code:: shell

   git clone git://kernel.ubuntu.com/ubuntu/ubuntu-maverick.git
   cd ubuntu-maverick
   git checkout -b mybisect origin/master

This creates a local copy of the maverick repository, and then creates a
local branch named *mybisect* for your tests.

`Full list of git repos. <http://kernel.ubuntu.com/git>`__

Take a look first to see what you can learn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The version which works is tagged Ubuntu-2.6.35-24.42. The version which
has the problem is tagged Ubuntu-2.6.35-25.43

First, lets take a quick look at the changes between the two:

.. code:: shell

   git log --oneline Ubuntu-2.6.35-24.42..Ubuntu-2.6.35-25.43

Now, how many commits are in there?

.. code:: shell

   git log --oneline Ubuntu-2.6.35-24.42..Ubuntu-2.6.35-25.43 | wc

It says 325, but two of those are the startnewrelease and final
changelog changes, so there are 323 commits, and the bad one is among
them.

Sometimes you can easily find the problem if it's in a subsystem that
only has changes from a few patches. In this example, it's Radeon
hardware that is affected, so try looking at the commits to the radeon
driver:

.. code:: shell

   git log --oneline Ubuntu-2.6.35-24.42..Ubuntu-2.6.35-25.43 drivers/gpu/drm/radeon/

That still shows eleven commits. Reverting each of those and testing
will take longer than bisecting the entire set of changes, so we'll go
ahead and do the bisection.

Determine the known good and known bad commits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the Maverick case we have:

Ubuntu-2.6.35-25.43 - <BAD>

Ubuntu-2.6.35-24.42 - <GOOD>

Start the bisection
^^^^^^^^^^^^^^^^^^^

Start a bisection by using the command **git bisect start <BAD>
<GOOD>**:

.. terminal::
   :input: git bisect start Ubuntu-2.6.35-25.43 Ubuntu-2.6.35-24.42

   Bisecting: 162 revisions left to test after this (roughly 7 steps)
   [dae1e6305dba4ff1e8574b3b6eb42613d409b460] olpc_battery: Fix endian neutral breakage for s16 values

This tells you that git has chosen the commit "olpc_battery: . . ." as
the midpoint for the first bisection, and reset your tree so that it is
the top commit. Git is also telling you that there are about seven
bisection steps left.

Give this test a version number
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you build this kernel for testing, you have to give it a version
number. This is done by editing the debian.master/changelog file.

The top of that file now appears like this:

::

   linux (2.6.35-25.43) UNRELEASED; urgency=low

     CHANGELOG: Do not edit directly. Autogenerated at release.
     CHANGELOG: Use the printchanges target to see the curent changes.
     CHANGELOG: Use the insertchanges target to create the final log.

    --  Tim Gardner <tim.gardner@canonical.com>  Mon, 06 Dec 2010 10:45:38 -0700

The top line of that file has the version in it. Choose a version that
is:

-  clearly a test

-  will be superceded by later kernels

-  has meaning to you in your bisection testing

I use my initials, plus an incrementing number, plus an indicator of the
launchpad bug associated with the problem - thus, my first test version
is:

2.6.35-25.44~spc01LP703553

The '~' is a special versioning trick that means that this kernel will
be superceded and replaced by any version higher than 2.6.35-25.44, yet
this version is considered higher than .44 - using this versioning makes
sure that if a user tests our kernel they won't keep it around after the
next update comes along.

You also need to change the UNRELEASED to the maverick pocket, or it
will not be accepted for your PPA build.

Edit the changelog and replace the entire text in the earlier box with
this:

::

   linux (2.6.35-25.44~spc01LP703553) maverick; urgency=low

     Test build for bisection of a Radeon regression

    --  Steve Conklin <sconklin@canonical.com>  Mon, 24 Jan 2011 22:45:38 -0600

Do not commit the change you just made to the changelog into your local
git repo. There's no need and it makes it harder to build subsequent
tests.

Now `build the
kernel <https://wiki.ubuntu.com/Kernel/BuildYourOwnKernel>`__. You can
use a PPA, but it will probably take a lot longer to build.

Getting test results
^^^^^^^^^^^^^^^^^^^^

Place the kernel package where your testers can get to it. Let them know
it's there. The Launchpad bug is a good place to track all of your
testing. You can review `the
bug <https://bugs.launchpad.net/ubuntu/+source/linux/+bug/703553>`__
used for the example again.

Using the test results
^^^^^^^^^^^^^^^^^^^^^^

when you have the test results, you run git bisect again and say whether
the test was good or bad. In this example case, the first test was bad,
so we do the following:

.. terminal::
   :input: git bisect bad

   Bisecting: 80 revisions left to test after this (roughly 6 steps)
   [1829af44f4fe8600d6c9cde5fcb7a1345b201eaf] r6040: Fix multicast filter some more

Now edit the changelog with a new version and build the next test.
Repeat until the bad commit is eventually identified.

At any time, you can use the command:

.. code:: shell

   git bisect log

to review all the work that's taken place.

FAQ
---

Pre-built Ubuntu kernels are missing some packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When attempting to install the pre-built Ubuntu kernels for version
bisecting, some files may be missing that seem to prevent one from
properly testing to the issue. For example, linux-modules-\* and
linux-modules-extra-\*. In this case, one will want to install the
linux-image-extra-\* package, and vice versa. If this doesn't work, one
will want to skip this kernel version, and test the next version past
this that has the required files.

Bisecting: a merge base must be tested
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If one performs at a terminal:

::

   git bisect start Ubuntu-2.6.38-8.40 Ubuntu-2.6.38-7.39
   Bisecting: a merge base must be tested
   [521cb40b0c44418a4fd36dc633f575813d59a43d] Linux 2.6.38

git is advising that in order to proceed with the bisect, one would need
to tell git if the commit 521cb40b0c44418a4fd36dc633f575813d59a43d is
good or bad via:

.. code:: shell

   git bisect good

or:

.. code:: shell

   git bisect bad

Map Ubuntu kernel to mainline kernel for mainline bisection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   If you have the issues below, or some other issue preventing
   you from further commit bisecting Ubuntu kernel versions, assuming the
   issue is not due to a downstream patch or configuration change, one
   would want to switch from commit bisecting the Ubuntu kernel to commit
   bisecting the mainline kernel. As the Ubuntu kernel and mainline kernel
   have differing version schemes, one would want to use the `Ubuntu to
   Mainline kernel version
   mapping <http://kernel.ubuntu.com/~kernel-ppa/info/kernel-version-map.html>`__
   page. With this is mind, it may not map to an upstream tag one could use
   directly for bisection. For example, if one is using Ubuntu kernel
   3.10.0-6.17, which maps to mainline 3.10.3, when one tries to bisect
   against this tag, one would get: fatal: Needed a single revision Bad rev
   input: v3.10.3

   Hence, one could simply just use an adjacent tag that is valid
   v3.10-rc7.

Commit bisecting Ubuntu kernel versions across non-linear tags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following will tell you whether or not two given tags are
non-linear:

.. code:: shell

   git rev-list <newer-tag> | \
   grep $(git log --pretty=oneline -1 <older-tag> | cut -d' ' -f1)

If that command outputs a sha1 then the tags are linear, otherwise they
are not. If they are not, this will cause the below mentioned folders to
disappear. Assuming the issue is not due to a downstream patch or
configuration change, one would want to switch from commit bisecting the
Ubuntu kernel to commit bisecting the mainline kernel following the
instructions below. You can use the `Ubuntu to Mainline kernel version
mapping <http://kernel.ubuntu.com/~kernel-ppa/info/kernel-version-map.html>`__
page to ease this transition.

Why did the folders debian and debian.master disappear?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example, while attempting to commit bisect the Ubuntu kernel for
Precise, if one performed the following:

.. code:: shell

   git clone git://kernel.ubuntu.com/ubuntu/ubuntu-precise.git && \
   cd ubuntu-precise && git checkout -b mybisect origin/master && \
   git log --oneline Ubuntu-3.2.0-14.23..Ubuntu-3.2.0-15.24 | wc && git bisect start Ubuntu-3.2.0-15.24 Ubuntu-3.2.0-14.23

one will notice the debian and debian.master folders disappeared. This
is a result of bisecting non-linear commits.

Commit bisecting the Ubuntu development release kernel
------------------------------------------------------

For an issue with the current development kernel, the bisect most likely
will be performed against `Linus'
tree <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/>`__:
git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git. However, for
`stable
kernels <https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/>`__,
a bisect is usually performed against the `linux-stable
tree <https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/>`__:
git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git. In some
cases, you may need to perform a bisect against an Ubuntu tree, such as
`ubuntu-bionic <https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/bionic>`__.

How do I bisect the upstream kernel?
====================================

Version bisecting upstream kernels
----------------------------------

All of the upstream kernels are published at
http://kernel.ubuntu.com/~kernel-ppa/mainline/. The first step in
the bisect process is to find the last "Good" kernel version, followed
consecutively in version by the first "Bad" one. That is done by
downloading, installing and testing kernels from
`here <http://kernel.ubuntu.com/~kernel-ppa/mainline/>`__. Once this is
done, the next step is commit bisecting upstream kernel versions.

Commit bisecting upstream kernels
---------------------------------

First, follow the
`KernelTeam/GitKernelBuild <https://wiki.ubuntu.com/Kernel/KernelBisection/KernelTeam/GitKernelBuild#>`__
guide to build a new kernel from git. The step you will be doing the
most is #9. "--append-to-version=-custom" is very important to change to
help differentiate your kernels.

As an example, let's say testing of the mainline kernel has shown the
regression was introduced somewhere between v3.2-rc1 and v3.2-rc2.

Confirmation of mainline test results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's not required, but if you are new to building a kernel I suggest
confirming your results by building both of the mainline builds you
narrowed it down to yourself. In our example this is v3.2-rc1 (good) and
v3.2-rc2 (bad).

For v3.2-rc1 you would test this by running:

.. code:: shell

   git checkout v3.2-rc1

Now run the build, install the kernel, and test your issue.

Start the bisect
~~~~~~~~~~~~~~~~

.. code:: shell

   git bisect start
   git bisect good v3.2-rc1
   git bisect bad v3.2-rc2

The bisect will then print out something like:

.. terminal::
   :input: git bisect start; git bisect good v3.2-rc1; git bisect bad v3.2-rc2

   Bisecting: 161 revisions left to test after this (roughly 7 steps)
   [fe10e6f4b24ef8ca12cb4d2368deb4861ab1861b] Merge branch 'for-linus' of git://git.kernel.org/pub/scm/linux/kernel/git/tiwai/sound

Basically what that is telling you is that commit
fe10e6f4b24ef8ca12cb4d2368deb4861ab1861b is approximately in the middle
of v3.2-rc1 and v3.2-rc2 and is a good candidate for testing.

Now run the build, install the kernel, and test your issue.

Does your issue still occur?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If testing was good (i.e. no issues) do the following:

.. code:: shell

   git bisect good

Otherwise if the testing was bad, you would do the following:

.. code:: shell

   git bisect bad

Repeat until done
~~~~~~~~~~~~~~~~~

Repeat the process: build, install, test, and report back test results
with git bisect good or bad.

You will know when it is done because it will display a message starting
with: 7fd2ae21a42d178982679b86086661292b4afe4a is the first bad commit

Please attach that entire message and the output of git bisect log (as a
file) to your bug report.

Start upstream bisect
~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

   git bisect start
   git bisect good v3.2-rc1
   git bisect bad v3.2-rc2

The bisect will then print out something like:

.. terminal::
   :input: git bisect start; git bisect good v3.2-rc1; git bisect bad v3.2-rc2

   Bisecting: 161 revisions left to test after this (roughly 7 steps)
   [fe10e6f4b24ef8ca12cb4d2368deb4861ab1861b] Merge branch 'for-linus' of git://git.kernel.org/pub/scm/linux/kernel/git/tiwai/sound

Basically what that is telling you is that commit
fe10e6f4b24ef8ca12cb4d2368deb4861ab1861b is approximately in the middle
of v3.2-rc1 and v3.2-rc2 and is a good candidate for testing. You now
want to build a kernel up through commit
fe10e6f4b24ef8ca12cb4d2368deb4861ab1861b.

To do this, you can use the mainline-build-one script which can be found
at ~kteam-tools/malinline-build/maineline-build-one .

Build upstream test kernel
~~~~~~~~~~~~~~~~~~~~~~~~~~

The next step is to run the mainline-build-one script. This script will
build an upstream kernel that will be able to install and run on a
Ubuntu system. Run the mainline-build-one script as follows (assuming
you've added kteam-tools/mainline-build to your PATH):

::

   mainline-build-one fe10e6f4b24ef8ca12cb4d2368deb4861ab1861b precise

This will generate a bunch of .debs one directory level above. One of
the debs will be something like:

::

   linux-image-3.2.0-0302rc1gfe10e6f-generic_3.2.0-0302rc1gfe10e6f.201112010256_amd64.deb

This is the deb you will want to test and see if the bug exists or not.

Update bisect with test results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Depending on your test results, you'll mark this commit as "good" or
"bad":

.. code:: shell

   cd linux-stable

If testing was good (i.e. no issues) do the following:

.. code:: shell

   git bisect good fe10e6f4b24ef8ca12cb4d2368deb4861ab1861b

Otherwise if the testing was bad, you would do the following:

.. code:: shell

   git bisect bad fe10e6f4b24ef8ca12cb4d2368deb4861ab1861b

That'll then spit out the next commit to test. Eventually you'll narrow
it down and the bisect will tell you which was the first bad commit.

Once the first bad commit is identified, you can then try reverting that
one commit and see if that fixes the bug.

FAQ
---

I mapped the Ubuntu kernel to the mainline kernel, but I can't reproduce the problem when testing the mainline kernel. What's going on?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible that a Ubuntu patch applied to the upstream kernel is
causing the bug. Hence, if one tests the upstream kernel, the problem
won't be reproducible.

How do I reverse bisect the upstream kernel?
============================================

A reverse bisect is just running the same methodology described above in
a slightly different way, to narrow down a potential fix identified
upstream. For example, let us assume you had a bug in Saucy kernel
3.11.0-15.23. Let us also assume the issue is not due to something in
the downstream/Ubuntu kernel (configuration, out-of-tree patch, etc.).
Then, you subsequently tested
`upstream <https://wiki.ubuntu.com/Kernel/MainlineBuilds>`__ kernel
v3.13-rc5 and identified the issue doesn't happen.
`Mapping <http://kernel.ubuntu.com/~kernel-ppa/info/kernel-version-map.html>`__
the Saucy kernel to upstream gives kernel 3.11.10. So, we now know the
issue exists at least as early as mainline 3.11.10 and is fixed in
v3.13-rc5. The next step is test the linux kernel from the Proposed
repository.

Reverse bisecting by testing the Proposed repository
----------------------------------------------------

As fixes for the linux kernel can be fast, by the time you start reverse
bisecting, the fix may have already been posted into the Proposed
repository. Hence, you will want to enable and test the kernel from the
Proposed repository following the instructions from
`here <https://wiki.ubuntu.com/Testing/EnableProposed>`__.

However, if the linux kernel from the Proposed repository doesn't fix
your issue, the next step is reverse bisecting upstream kernel versions.

Reverse bisecting upstream kernel versions
------------------------------------------

The first step is to find the last bad upstream kernel version, followed
consecutively by the first good one. This is done by downloading,
installing and testing mainline kernels from
`here <https://wiki.ubuntu.com/Kernel/MainlineBuilds>`__. So, looking at
the list we have:

+-------------------+
| v3.13-rc5-trusty/ |
|                   |
| v3.13-rc4-trusty/ |
|                   |
| v3.13-rc3-trusty/ |
|                   |
| v3.13-rc2-trusty/ |
|                   |
| v3.13-rc1-trusty/ |
|                   |
| v3.12.6-trusty/   |
|                   |
| v3.12.5-trusty/   |
|                   |
| v3.12.4-trusty/   |
|                   |
| v3.12.3-trusty/   |
|                   |
| v3.12.2-trusty/   |
|                   |
| v3.12.1-trusty/   |
|                   |
| v3.12-trusty/     |
|                   |
| v3.12-saucy/      |
|                   |
| v3.12-rc7-saucy/  |
|                   |
| v3.12-rc6-saucy/  |
|                   |
| v3.12-rc5-saucy/  |
|                   |
| v3.12-rc4-saucy/  |
|                   |
| v3.12-rc3-saucy/  |
|                   |
| v3.12-rc2-saucy/  |
|                   |
| v3.12-rc1-saucy/  |
|                   |
| v3.11.10.1-saucy/ |
|                   |
| v3.11.10-saucy/   |
+-------------------+

The midpoint release is v3.12.1-trusty. One would continue to test the
successive midpoints of each result, until we have the first bad
version, followed consecutively by the first good version. Let us assume
this was narrowed down to v3.13-rc4 as the bad, and v3.13-rc5 as the
good. The next step is reverse commit bisecting upstream kernel
versions.

Reverse commit bisecting upstream kernel versions
-------------------------------------------------

Now one will utilize the git skills learned
`above <https://wiki.ubuntu.com/Kernel/KernelBisection#Commit_bisecting_upstream_kernel_versions>`__
in a slightly different way. This is due to how git was designed with
forward bisections in mind. However, one may utilize git to accomplish a
reverse bisect. So, once Linus's development tree has been cloned:

.. code:: shell

   git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git && cd linux

one would execute at a terminal:

.. code:: shell

   git checkout v3.13-rc5
   git bisect start
   git bisect good v3.13-rc4
   git bisect bad v3.13-rc5 

Please notice how v3.13-rc4 was marked good (even though we tested it to
be bad) and v3.13-rc5 was marked bad. This is intentional. If the commit
one `builds <https://wiki.ubuntu.com/KernelTeam/GitKernelBuild>`__
against next works, one will mark this bad. One will continue this
process until the fix commit is identified.

Testing a newly released patch from upstream
============================================

Lets assume you may have identified a newly released upstream patch that
may address your issue, but hasn't been commited to the upstream
development tree yet. Let us take as an example the following upstream
patch noted
`here <http://www.spinics.net/lists/linux-acpi/msg47755.html>`__.

Start copying from the line where it notes:

.. code:: shell

   diff --git a/drivers/acpi/video.c b/drivers/acpi/video.c

to the last code line before the double dash:

.. code:: c

    static int register_count;

Your patch file should be exactly as shown, honoring all spaces, or lack
thereof:

.. code:: diff

   diff --git a/drivers/acpi/video.c b/drivers/acpi/video.c
   index 995e91b..b3032f8 100644
   --- a/drivers/acpi/video.c
   +++ b/drivers/acpi/video.c
   @@ -85,7 +85,7 @@ module_param(allow_duplicates, bool, 0644);
     * For Windows 8 systems: if set ture and the GPU driver has
     * registered a backlight interface, skip registering ACPI video's.
     */
   -static bool use_native_backlight = false;
   +static bool use_native_backlight = true;
    module_param(use_native_backlight, bool, 0644);

    static int register_count;

save this file to your Desktop as testfix.patch. Then execute at a
terminal:

.. code:: shell

   git config --global user.email "you@example.com" && git config --global user.name "Your Name" && cd $HOME && git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git && patch ~/linux/drivers/acpi/video.c ~/Desktop/testfix.patch && cd linux && git add . && git commit

Now in the new window type:

::

   example

on your keyboard press :kbd:`Ctrl+O` → :kbd:`Enter` → :kbd:`Ctrl+X`. Then, type at a
terminal:

.. code:: shell

   cp /boot/config-`uname -r` .config && yes '' | make oldconfig && make clean && make -j `getconf _NPROCESSORS_ONLN` deb-pkg LOCALVERSION=-custom && cd .. && sudo dpkg -i *.deb && git fetch origin;git fetch origin master;git reset --hard FETCH_HEAD

If for whatever reason the new kernel doesn't boot, it may not be you
did something wrong, but just that it won't boot with this commit
applied, or the configuration file choices were not tested against it.

Bisecting via mainline-build-one (Advanced users only)
======================================================

If you are new to bisecting, then feel free to ignore this section.
However, if you will be doing upstream testing often (i.e. not just
bisecting your one problem, and then may never bisect again) this is
provided as a convenience. You need to set up your system first, which
is not described here.

Previously, this article talked about bisecting a Ubuntu Linux kernel.
Now you may be wondering how to use mainline-build-one to go about
bisecting and building an upstream kernel. This is where you can make
use of the mainline build scripts, which are available from the
kteam-tools repository
http://kernel.ubuntu.com/git/ubuntu/kteam-tools.git. As an
example, let's say testing of the mainline kernel has shown the
regression was introduced somewhere between v3.2-rc1 and v3.2-rc2. The
next section will show you the steps to perform a bisect and build a
test kernel.

Login to a machine that you've configured to build kernels and setup environment
--------------------------------------------------------------------------------

Clone the appropriate tree. For example, Linus' stable-tree for stable
kernels:

.. code:: shell

   git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git linux-stable

Note, one could also use Linus' development tree for development
kernels.

Clone the kteam-tools repository:

.. code:: shell

   git clone git://kernel.ubuntu.com/ubuntu/kteam-tools.git kteam-tools

Change into the kernel tree directory:

.. code:: shell

   cd linux-stable

Add a remote repository to the Ubuntu release you are building your
kernel for. This allows you to get all the debian specific bits
(debian.master for example). In this example it will be Xenial:

.. code:: shell

   git remote add xenial git://kernel.ubuntu.com/ubuntu/ubuntu-xenial.git

Questions about mainline-build-one?
-----------------------------------

If you have questions about the mainline-build-one, please ask the
`Ubuntu Kernel Team <https://wiki.ubuntu.com/KernelTeam>`__, as they are
the maintainers of this resource.

External links
==============

-  Fighting regressions with git bisect -
   http://www.kernel.org/pub/software/scm/git/docs/git-bisect-lk2009.html
