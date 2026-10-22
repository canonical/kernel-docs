---
myst:
  html_meta:
    description: "Learn how to bisect the Ubuntu kernels when ivestigating a bug"
---

```{owners} bjamison
```

## Introduction

If you are reading this because you were referred here to bisect your kernel, or you want to know more about kernel bisecting, then you are taking the best route to get your bug resolved as soon as possible. This article is written with the intention that any one at any skill level may go from start to finish successfully, working through each section one at a time. If you get stuck, please feel free to ask for [help](https://ubuntu.com/support/community-support).

## What is a bisect?

A bisect (sometimes called a forward bisect), is the fastest process of finding the midpoint between a known good software version release, and a known bad one released afterwards. One continues finding the successive midpoint until the last good software version release followed consecutively by the first bad one is identified.

Performing a bisect is faster than testing every version in between the initial known good version, and the known bad one. For example, if your known good release was 1.0, and bad was 1.10, the worst case scenario is testing 9 releases (1.1, 1.2, 1.3, ..., 1.9) until 1.9 was found to be the last known good version. However, bisecting the worst case scenario, one would test only 4 releases (1.5, 1.7, 1.8, and 1.9).

## What is a reverse bisect?

A reverse bisect is the process of finding the midpoint between a known bad software version release, and a known good one released afterwards. One continues finding the successive midpoint until the last bad software version release followed consecutively in version by the first good one is identified.

## How do I bisect a Ubuntu kernel bug?

For example, you started with a fully updated 24.04 Noble Numbat install using kernel 6.8 and you had no problem. Then, instead of upgrading you just did a clean install of 26.04 Resolute Racoon, and found what appears to be a [linux](https://launchpad.net/ubuntu/+source/linux) kernel bug. Hence, to confirm this is a regression in the linux kernel, to rule out a user space issue, and to identify the specific regression, the next step is release bisecting Ubuntu.

### Release bisecting Ubuntu

To find the introduction point of the bug first narrow down the first Ubuntu release after Noble that this problem began in. The midpoint release between Noble and Resolute is 25.10 Questing Quokka. These releases are downloadable from [http://releases.ubuntu.com/](http://releases.ubuntu.com/). If the bug is reproducible in Questing, then the regression happened going from Noble to Questing, and the next step is version bisecting Questing. Inversely, if the bug is not reproducible in Questing, then Resolute is responsible for the regression.

```
26.04 Resolute Racoon  (known bad)
25.10 Questing Quokka
24.04 Noble Numbat     (known good)
```

### Version bisecting Ubuntu kernels

Continuing the prior example, the next step is to find the last good kernel version, followed consecutively in version by the first bad one. So, assuming the Noble kernel was kept updated, as per [https://launchpad.net/ubuntu/noble/+source/linux](https://launchpad.net/ubuntu/noble/+source/linux), the last Noble kernel version published for upgrade as of May 20, 2026 was 6.8.0-130.130. Next, assuming the kernel bug was found in the most recent kernel version released for Questing, 6.17.0-38.38 becomes our oldest known failing version.

```
Questing  6.17.0-38.38    (oldest known fail)
          6.17.0-35.35
          ...
          6.17.0-9.9
          ...
          6.15.0-3.3
          6.14.0-15.15
Noble     6.8.0-130.130   (newest known pass)
```

The next step is to install kernel 6.17.0-9.9 (the midpoint between the first release of Questing and the most recent). 

After going to the page for your selected kernel version, click **amd64**. On the build page under **Build files**
you will find the files needed to install the kernel, see [here](https://wiki.ubuntu.com/Kernel/MainlineBuilds) for instructions on how to do this.

If the bug is reproducible, you now know that the Ubuntu kernel bug was introduced between 6.17.0-9.9 and 6.14.0-15.15. Repeat these steps, once the guilty kernel version has been determined the next step is commit bisecting the kernel.

### Commit bisecting Ubuntu kernels

#### What do I need to build and commit bisect Ubuntu kernels?

The rest of this page assumes that you know how to fetch a kernel from the Ubuntu git repository and build it. If you can't do that yet, try starting with [this wiki page](https://wiki.ubuntu.com/Kernel/BuildYourOwnKernel). 

#### Example of commit bisecting Ubuntu kernels

The commands in the example on this page use a real life example. In January of 2011, a kernel which was published to the -proposed pocket caused Radeon graphics to break for a number of users. Typing the commands as shown on this page will recreate the steps taken to find the bad commit in that release. The entire history of testing the bisected kernels for that regression [appears in the bug](https://bugs.launchpad.net/ubuntu/+source/linux/+bug/703553).

##### Getting set up

You need to have a bug reproducer, or have a cooperative tester in the community. If you can't reliably determine whether the bug exists in a given kernel, bisection will not give meaningful results. This process goes a lot faster if you can quickly build kernels and have them tested. Using a fast build machine and having good communications with the testers will speed things up.

##### Take a look first to see what you can learn

The version which works is tagged Ubuntu-2.6.35-24.42.
The version which has the problem is tagged Ubuntu-2.6.35-25.43

First, lets take a quick look at the changes between the two:

```
git log --oneline Ubuntu-2.6.35-24.42..Ubuntu-2.6.35-25.43
```

Now, how many commits are in there?

```
git log --oneline Ubuntu-2.6.35-24.42..Ubuntu-2.6.35-25.43 | wc
```

It says 325, but two of those are the opening and closing commits, so there are 323 commits, and the bad one is among them.

Sometimes you can easily find the problem if it's in a subsystem that only has changes from a few patches.
In this example, it's Radeon hardware that is affected, so try looking at the commits to the Radeon driver:

```
git log --oneline Ubuntu-2.6.35-24.42..Ubuntu-2.6.35-25.43 drivers/gpu/drm/radeon/
```

That still shows eleven commits. Reverting each of those and testing will take longer than bisecting the entire set of changes, so we'll go ahead and do the bisection.

##### Determine the known good and known bad commits

In the Maverick case we have:

```
Ubuntu-2.6.35-25.43 = BAD
Ubuntu-2.6.35-24.42 = GOOD
```

##### Start the bisection

Start a bisection with `git bisect start`.

```
git bisect start Ubuntu-2.6.35-25.43 Ubuntu-2.6.35-24.42

Bisecting: 162 revisions left to test after this (roughly 7 steps)
[dae1e6305dba4ff1e8574b3b6eb42613d409b460] olpc_battery: Fix endian neutral breakage for s16 values
```

This tells you that git has chosen the commit "olpc_battery: . . ." as the midpoint for the first bisection, and reset your tree so that it is the top commit. Git is also telling you that there are about seven bisection steps left.

##### Give this test a version number

Before you build this kernel for testing, you have to give it a version number. This is done by editing the debian.master/changelog file.

The top of that file now appears like this:

```
linux (2.6.35-25.43) UNRELEASED; urgency=low

  CHANGELOG: Do not edit directly. Autogenerated at release.
  CHANGELOG: Use the printchanges target to see the curent changes.
  CHANGELOG: Use the insertchanges target to create the final log.

 --  Tim Gardner <tim.gardner@canonical.com>  Mon, 06 Dec 2010 10:45:38 -0700
```

The top line of that file has the version in it. Choose a version that is:

- clearly a test
- will be superseded by later kernels
- has meaning to you in your bisection testing

For example use an incrementing number, plus an indicator of the launchpad bug associated with the problem:

```
2.6.35-25.44~01LP703553
```

The '~' is a special versioning trick that means that this kernel will be superseded and replaced by any version higher than 2.6.35-25.44, yet this version is considered higher than .44 - using this versioning makes sure that if a user tests our kernel they won't keep it around after the next update comes along.

You also need to change the UNRELEASED to the maverick pocket, or it will not be accepted for your PPA build.

Edit the changelog and replace the entire text in the earlier box with this:

```
linux (2.6.35-25.44~01LP703553) maverick; urgency=low

  Test build for bisection of a Radeon regression

 --  Steve Conklin <sconklin@canonical.com>  Mon, 24 Jan 2011 22:45:38 -0600
```

Do not commit the change you just made to the changelog into your local git repository. There's no need and it makes it harder to build subsequent tests.

Now [build the kernel](https://wiki.ubuntu.com/Kernel/BuildYourOwnKernel). You can use a PPA, but it will probably take a lot longer to build.

##### Using the test results

Place the kernel package where your testers can get to it, and let them know it's there. The Launchpad bug is a good place to track all of your testing. When you have the test results, you run git bisect again and say whether the test was good or bad. In this example case, the first test was bad, so we do the following:

```
git bisect bad
```

And git responds with:

```
Bisecting: 80 revisions left to test after this (roughly 6 steps)
[1829af44f4fe8600d6c9cde5fcb7a1345b201eaf] r6040: Fix multicast filter some more
```

Now edit the changelog with a new version and build the next test. Repeat until the bad commit is eventually identified.

At any time, you can use the command `git bisect log` to review all the work that's taken place.

## How do I bisect the upstream kernel?

All of the upstream kernels are published at [http://kernel.ubuntu.com/~kernel-ppa/mainline/](http://kernel.ubuntu.com/~kernel-ppa/mainline/). Using the same philosophy from bisecting Ubuntu kernels find the last "Good" kernel version, followed consecutively in version by the first "Bad" one, continue commit bisecting within the target kernel version until you have identified the commit that introduced the bug.

### FAQ

#### Pre-built Ubuntu kernels are missing some packages

When attempting to install the pre-built Ubuntu kernels for version bisecting, some files may be missing that seem to prevent one from properly testing to the issue. For example, `linux-modules-*` and `linux-modules-extra-*`. In this case, install the `linux-image-extra-*` package, and vice versa. If this doesn't work, skip this kernel version, and test the next version past this that has the required files.

#### Bisecting: a merge base must be tested

If you get this result from running `git bisect start`

```
git bisect start Ubuntu-2.6.38-8.40 Ubuntu-2.6.38-7.39

Bisecting: a merge base must be tested
[521cb40b0c44418a4fd36dc633f575813d59a43d] Linux 2.6.38
```

 git is advising that in order to proceed with the bisect, you need to tell git if the commit 521cb40b0c44418a4fd36dc633f575813d59a43d is good or bad via:

```
git bisect good
```

 or:

```
git bisect bad
```

##### Commit bisecting Ubuntu kernel versions across non-linear tags

The following will tell you whether or not two given tags are non-linear:

```
git rev-list <newer-tag> | \
grep $(git log --pretty=oneline -1 <older-tag> | cut -d' ' -f1)
```

If that command outputs a sha1 then the tags are linear, otherwise they are not.  If they are not, this will cause the `debian` and `debian.master` directories to disappear. Assuming the issue is not due to a downstream patch or configuration change, you would want to switch from commit bisecting the Ubuntu kernel to commit bisecting the mainline kernel.

#### Map Ubuntu kernel to mainline kernel for mainline bisection

If you have some issue preventing you from further commit bisecting Ubuntu kernel versions, assuming the issue is not due to a downstream patch or configuration change, you would want to switch from commit bisecting the Ubuntu kernel to commit bisecting the mainline kernel. The Ubuntu kernel and mainline kernel have differing version schemes, so take care to select the correct one. With this is mind, it may not map to an upstream tag you could use directly for bisection. For example, if you are using Ubuntu kernel 3.10.0-6.17, which maps to mainline 3.10.3, when you try to bisect against this tag, you get:

```
fatal: Needed a single revision
Bad rev input: v3.10.3
```

In this case use an adjacent tag that is valid, like v3.10-rc7.
