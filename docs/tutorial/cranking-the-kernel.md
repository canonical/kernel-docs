# Turning the Crank

## Introduction

In this tutorial, we will crank an Ubuntu kernel, which means to apply updates to an existing derivative Ubuntu kernel from its parent kernel, package it, and prepare it for testing.

[cranky](https://kernel.ubuntu.com/gitea/kernel/kteam-tools/src/branch/master/cranky) is a toolchain which assists in all of these steps.

### Table of Contents/Steps in this Guide

The steps of cranking a kernel are relatively straightforward:

1. Set Up/Update Environment
2. Download Current Version of the Kernel
3. Apply Updates from the Upstream Kernel 
4. Verify the Kernel Builds Successfully
5. Package the kernel for Release
6. Upload kernel for release/review

---

<!-- TODO specify the SRU cycle -->
In this tutorial, we will crank a 24.04 LTS (Noble Numbat) (codename `noble`) Google cloud kernel (codename `linux-gke`). Keep these codenames in mind for future commands.

Learn more about Ubuntu releases and derivative kernels [here](TODo).


## 1. Set Up/Update Environment

First, follow the [Cranky Environment Setup](TODO) tutorial.

### chroot environment
We use [chroot](https://en.wikipedia.org/wiki/Chroot) environments to isolate different sets of tools when kernel cranking. cranky helps us set up and manage these chroot jails.

If it's our first time creating a chroot for this release (Noble Numbat), we must first create the chroot base:
```bash
cranky chroot create-base noble:linux-gke
```
This will output a lot of text as it installs various packages needed for the chroot to work properly. (It took ~20 minutes to complete.)

Next, create the chroot session:
```bash
cranky chroot create-session noble:linux-gke
```

This will also output a lot of text as it uses apt to install various packages needed for the crank. (It took ~2 minutes to complete.)

<!-- TODO can we be more specific about what each command does? Why are they separate if the descriptions are basically identical? -->

### Update kteam-tools
Finally, update your local clone of kteam-tools to the latest commit on the main branch:

```bash
cd ~/canonical/kteam-tools/
git pull
```

## 2. Download Current Version of the Kernel
Next, clone the chosen kernel in its current state.

<!-- TODO is the cd required? Or does cranky checkout default to this dir? -->
<!-- TODO this probably needs SRU cycles specified so it's more reproducible. -->
```bash
cd ~/canonical/kernel/ubuntu/
cranky checkout noble:linux-gke
```

Once this command is finished (It took ~20 minutes to complete), you should see the following directories inside the newly-created `./noble/linux-gke/` directory:
- `linux-lrm/` <!-- TODO delete when moving to linux-gke -->
- `linux-main/`: The actual Linux kernel source
- `linux-meta/` <!-- TODO describe --> 
- `linux-signed/`: Canonical's kernel signing stuff <!-- TODO describe better --> 


## 3. Apply Updates from the Upstream Kernel 
The upstream kernel will have updates that should be propagated down to this kernel.

### 3.1. Fix helper scripts
Update the local (in-tree) helper scripts cranky uses to the latest version:
```bash
cd ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main/
cranky fix
```
You should see some output showing that cranky executed several scripts.


### 3.2. Rebase on top of updated parent
Because this is a derivative kernel, we need to apply updates from its parent, the generic kernel:

```bash
cranky rebase
```

:::{tip}
For non-derivative kernels (e.g., `noble:linux`), this step is not required, and doesn't do anything.
:::

### 3.3. Fix helper scripts (again)
Sometimes after a `cranky rebase`, the helper scripts get updated. It's good practice to always re-run:

```bash
cranky fix
```

<!-- TODO what should this section be called? -->
## TODO new section
### Starting commit

<!-- TODO this section doesn't really explain why we are doing these things. Learn what's going on and then document better. -->

Run the following command:

```bash
cranky open
```

This command downloads ABI files <!--TODO what are ABI files? Link to an explanation--> from the previous release.

This also creates a new commit. Run `git show` and see that this new commit starts with "UBUNTU: Start new release" and shows an update to `./debian.gke/changelog`.


### Review 
Sometimes the rebase doesn't get all the changes. Run this command to manually review any outstanding changes:
```bash
cranky review-master-changes
```
<!-- TODO what does the output look like? -->

In particular, check if any changes were made to `debian.master/rules.d/` that
should be reflected in `debian.aws/rules.d/`. Those commits may not be
obvious in the master changelog.

<!-- TODO reword this to be more command-like and accurate -->
In the event of a config change in the derivative, this commit title is
used: "UBUNTU: \[Config\] <derivative>: Whatever title",
i.e "UBUNTU: \[Config\] aws: Whatever title".
This is useful in the changelog to make the distiction between a config
change in the parent vs a change in the derivative.

### Link to the Launchpad Bug Tracker

Run the following command to link this kernel to its corresponding Launchpad bug tracker:

:::{caution}
Use `--dry-run` unless you are actually cranking a kernel. Otherwise, this will overwrite Launchpad and might make destructive changes!
:::

```bash
cranky link-tb --dry-run
```

<!-- TODO describe output of dry run, it crashed on mine for some reason -->

### Update DKMS Packages
```bash
cranky update-dkms-versions
```

<!-- TODO describe output -->

### Closing commit
This step creates one final commit before a release is prepared. Run:
```bash
cranky close
```
<!-- TODO describe output -->

## 4. Verify the Kernel Builds Successfully
### Cloud Builder 
Connect to the canonical VPN. Then, run:

<!-- TODO add git remote add cbd -->

<!-- WARNING: cbd is internal only (so it seems)! What should we put here instead? -->

```bash
git push cbd
```

<!-- TODO describe output -->
<!-- TODO describe ssh -->

## 5. Package the kernel for Release
Run the following command:
<!--TODO add note that it's "dependents", not "dependent". -->
```bash
cranky update-dependents
```

### Tag commit
```bash
cranky tags
```
<!-- TODO describe output -->

### Verify Preparation
```bash
cranky verify-release-ready
```

The `tag pushed: warning` is an expected warning if you do not have commit rights.

### Pull sources

```bash
cd ..
# CWD == ~/canonical/kernel/noble/linux-gke/

cranky pull-sources noble:linux-gke --latest
```

### Build Sources
```bash
cd linux-main/
cranky build-sources
```

## Review
```bash
cd ..
# CWD == ~/canonical/kernel/noble/linux-gke/
cranky review *.changes
```

## Upload

<!-- TODO take note of SRU cycle earlier in the process -->

Normally, at this point a cranker with upload rights would publish the newly-cranked kernel to its PPA, which automatically kicks off boot testing.
However, without upload rights, we can request someone with rights to review our work, and publish the kernel on our behalf.

We can push the created files to a server that is accessible to the reviewer, like `kathleen`.
<!-- TODO is this canonical-only? -->

```bash
cd linux-main/
cranky push-review -s 2024.10.08 kathleen
```
