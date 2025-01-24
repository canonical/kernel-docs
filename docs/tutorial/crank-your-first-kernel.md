# Tutorial: Crank your first kernel

Cranking an Ubuntu kernel is the process of applying patches and updates to an existing Ubuntu kernel, packaging it, and preparing it for testing.
All this is done using the [cranky](https://kernel.ubuntu.com/gitea/kernel/kteam-tools/src/branch/master/cranky) toolchain.

<!-- TODO specify the SRU cycle -->
In this tutorial, we will crank a 24.04 LTS (Noble Numbat) (codename `noble`) Google cloud kernel (codename `linux-gke`).

```{tip}
 Keep these codenames handy for future commands.
```

## Prerequisites

You will need to complete the prerequisite setup below before proceeding with the tutorial:

- {doc}`Set up your cranky environment </how-to/cranking/set-up-cranky-environment>`
- Set up your [VPN connection]
- Get access to [Kernel team build resources]

## Set up and update build environment

First, we will prepare our build environment and tooling needed for cranking a kernel.

### Update chroot environment - `cranky chroot`

We use [chroot](https://en.wikipedia.org/wiki/Chroot) environments to isolate different sets of tools when doing kernel cranking.
`cranky` helps us set up and manage these chroot jails.

Creating the chroot jail is done in two steps. First, create the chroot base:

```bash
cranky chroot create-base noble:linux-gke
```

This can take several minutes to complete.
If successful, you should observe the various packages being installed and set up in the terminal output.

Next, create the chroot session:

```bash
cranky chroot create-session noble:linux-gke
```

This step uses APT to install various packages needed for the crank and may take several minutes to complete.

### Update kteam-tools repository

Update your local clone of `kteam-tools` to the latest commit on the `master` branch:

```{warning}
If your `kteam-tools` tree isn't clean, be sure to save your work before running the commands as this step will modify the repository.
Git should warn you if any destructive actions might occur.
```

```bash
cd ~/canonical/kteam-tools/
git switch master
git pull
```

Once the command completes successfully, you've got the latest version of cranky.

## Download current version of kernel - `cranky checkout`

You're now ready to clone the `linux-gke` kernel in its current state.

<!-- TODO this probably needs SRU cycles specified so it's more reproducible. -->

```bash
cranky checkout noble:linux-gke
```

This command can take several minutes to complete.

If the command completes successfully, you should see the following new directory: `~/canonical/kernel/ubuntu/noble/linux-gke/`.

Inside, there should be three git repositories cloned: `linux-main/`,  `linux-meta`, and `linux-signed`.

For more information, see {term}`linux-meta` and {term}`linux-signed` in the glossary.

## Apply updates from upstream kernel

The upstream kernel will possibly have changes that should be propagated down to this kernel.

### Fix helper scripts - `cranky fix`

Update the local (in-tree) helper scripts cranky uses to the latest version:

```bash
cd ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main/
cranky fix
```

You should see that cranky executed several scripts and go through the updating process for various scripts in the output terminal.

### Rebase on top of updated parent - `cranky rebase`

As `linux-gke` is a derivative kernel, we need to apply updates from its parent, the generic kernel:

```bash
cranky rebase
```

```{tip}
For non-derivative kernels (e.g., `noble:linux`), this step is not required.
```

### Fix helper scripts (again) - `cranky fix`

Sometimes after a `cranky rebase`, the helper scripts get updated.
It's good practice to always re-run:

```bash
cranky fix
```

## Commit and review updates

Now that we've pulled in all the upstream changes, we are ready to review and apply the commits to the `linux-gke` kernel.

### Add starting commit - `cranky open`

Create a commit that signifies the start of a new release.
This new commit will contain {term}`ABI` changes and any customization required by backport kernels.

```bash
cranky open
```

You should observe something similar in the output terminal:

```{terminal}
:input: cranky chroot create-base noble:linux-gke
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main

[...]
/home/kernel-engineer/canonical/kteam-tools/cranky/cranky startnewrelease --commit
Creating new changelog set for 6.8.0-1018.22...
[cranky/master-next 7c8a6e1e1f8b] UBUNTU: Start new release
 1 file changed, 8 insertions(+)


***** Now please inspect the commit before pushing *****
```

Run `git show` to verify that this new commit starts with "UBUNTU: Start new release" and shows an update to {file}`./debian.gke/changelog`.

```{terminal}
:input: git show
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main

Author: kernel-engineer <kernel.engineer@canonical.com>
Date:   Mon Jan 20 16:55:52 2025 +0800

    UBUNTU: Start new release
    
    Ignore: yes
    Signed-off-by: kernel-engineer <kernel.engineer@canonical.com>

diff --git a/debian.gke/changelog b/debian.gke/changelog
[...]
```

### Review rebased changes - `cranky review-master-changes`

Sometimes the rebase doesn't get all the changes.
So we need to run this command to manually review any outstanding changes:

```bash
cranky review-master-changes
```

This command will output any outstanding changes in a list with their commit hashes and descriptions.
Use `git show <commit-hash>` to view the changes.

```{terminal}
:input: cranky review-master-changes
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main

Listing changes in "debian.master/" since 9f8080a647a9e2c8c9a52b3e471b3f22d4dc0c67...

851f47333771 UBUNTU: [Packaging] debian.master/dkms-versions -- update from kernel-versions (main/2025.01.13)
41b4e628ce36 UBUNTU: Upstream stable to v6.6.55, v6.10.14
1de0f53d2545 UBUNTU: [Config] updateconfigs for MICROSOFT_MANA
547230d18843 UBUNTU: [Config] updateconfigs for deprecated CONFIG_Z3FOLD
1b64b00b69b7 UBUNTU: [Config] updateconfigs to set ILLEGAL_POINTER_VALUE for riscv64
14549d19d4b5 UBUNTU: [Config] updateconfigs to select PROC_MEM_ALWAYS_FORCE
3eb67a5e5da8 UBUNTU: [Packaging] Add list of used source files to buildinfo package
3b9e978a6cb4 UBUNTU: [Packaging] Sort build dependencies alphabetically
18d768dbc001 UBUNTU: Upstream stable to v6.6.54, v6.10.13
0861dae772cb UBUNTU: [Config] update configs for CONFIG_CRYPTO_AES_GCM_P10
82fbe5ae5484 UBUNTU: Upstream stable to v6.6.53, v6.10.12
```
<!-- TODO add a link to a reference on more info about when commits should be added -->

Since there are commits that have kernel config changes (e.g. commits with the "UBUNTU: [Config]" prefix), this will require an additional commit from our side.
We will address this in the `cranky close` step a little later.

### Link to Launchpad bug tracker - `cranky link-tb`

Run the following command to update the corresponding Launchpad tracking bug to this new kernel version being created.

```{warning}
Use `--dry-run` unless you are actually cranking a kernel.
Otherwise, this will overwrite Launchpad and might make destructive changes!
```

```bash
cranky link-tb --dry-run
```

```{tip}
If you are running `cranky link-tb` for the first time, you will be directed to the "Authorize application to access Launchpad on your behalf" page.
Choose your preferred option before continuing.
```

This step should update the Launchpad tracking bug -- which, among other things, will be used as an input for subsequent steps -- and create a git commit.

But since we used the `--dry-run` option for this tutorial, no changes are made to the local tree and no commit is created.

```{terminal}
:input: cranky link-tb --dry-run
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main

(This is a dry-run)
LP: #2093652 (noble/linux-gke: <version to be filled> -proposed tracker) 2025.01.13-1
Dry Run -- no changes made
```

### Update DKMS packages - `cranky update-dkms-versions`

The `debian.master/dkms-versions` file specifies dkms modules to be packaged with its kernel.
This command updates the package versions in `debian.gke/dkms-versions` to match the ones expected for the SRU cycle.

```bash
cranky update-dkms-versions
```

Since no changes are needed at this time, you should observe the following output:

```{terminal}
:input: cranky update-dkms-versions
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main

[...]

debian.gke/dkms-versions: No changes from kernel-versions
```

```{tip}
In most cases, no changes are expected as the up-to-date DKMS versions should have been committed on the generic kernel and picked up by the derivative or backport on rebase. 
```

### Add closing commit - `cranky close`

We will now create one final commit before preparing a release by running:

```bash
cranky close
```

This command, among several other things, closes the changelog, verifies changes are handled properly,
and makes a new commit signifying the cranked kernel.

Since there are config-related changes, `cranky close` is expected fail at this point.
You should observe a similar error in the terminal output stating that there were changes in `debian.gke/config/annotations`.

```{terminal}
:input: cranky close
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main

[...]

check-config: loading annotations from debian.gke/config/annotations
check-config: CONFIG_NVME_KEYRING changed from m to y: policy<{'amd64': 'm', 'arm64': 'm', 'armhf': 'm', 'ppc64el': 'm', 'riscv64': 'm', 's390x': 'm'}>)
check-config: 1 config options have been changed, review them with `git diff`
ERROR: 2 config-check failures detected

Importing all configurations ...

* Import configs for amd64-gke ...
* Import configs for arm64-gke ...
make: *** [debian/rules.d/1-maintainer.mk:31: updateconfigs] Error 1
Script failed
ERROR: Command failed: chroot (args=['run', '--', 'fakeroot', 'debian/rules', 'clean', 'updateconfigs'])
ERROR: Command failed: fdr (args=['clean', 'updateconfigs'])
ERROR: Command failed: close (args=[])
```

```{note}
If there were no unreviewed changes, skip ahead to the next section.
```

We will need to manually review and commit these changes with a descriptive
message of the updated config:

```bash
git add debian.gke/config/annotations
git commit -m "UBUNTU [Config] gke: Update CONFIG_NVME_KEYRING" -s
```

Finally, re-run `cranky close`.

```bash
cranky close
```

If successful, you should see a new commit when you run `git show`:

```diff
commit 6c9a5055b22f4c30aa3ba0c9df306762edb29197 (HEAD -> cranky/master-next)
Author: Kernel Engineer <kernel.engineer@canonical.com>
Date:   Wed Jan 15 12:42:31 2025 -0500

    UBUNTU: Ubuntu-gke-6.8.0-1017.21
    
    Signed-off-by: Kernel Engineer <kernel.engineer@canonical.com>

diff --git a/debian.gke/changelog b/debian.gke/changelog
index ba1191ce3bc2..a9ccd0b375a6 100644
--- a/debian.gke/changelog
+++ b/debian.gke/changelog
@@ -1,10 +1,18 @@
-linux-gke (6.8.0-1017.21) UNRELEASED; urgency=medium
+linux-gke (6.8.0-1017.21) noble; urgency=medium
 
-  CHANGELOG: Do not edit directly. Autogenerated at release.
-  CHANGELOG: Use the printchanges target to see the curent changes.
-  CHANGELOG: Use the insertchanges target to create the final log.
+  * noble/linux-gke: 6.8.0-1017.21 -proposed tracker (LP: #2093494)
 
- -- Kernel Engineer <kernel.engineer@canonical.com>  Wed, 15 Jan 2025 12:04:33 -0500
+  [ Ubuntu: 6.8.0-52.53 ]
+
+  * noble/linux: 6.8.0-52.53 -proposed tracker (LP: #2093521)
+  * CVE-2024-53164
+    - net: sched: fix ordering of qlen adjustment
+  * CVE-2024-53141
+    - netfilter: ipset: add missing range check in bitmap_ip_uadt
+  * CVE-2024-53103
+    - hv_sock: Initializing vsk->trans to NULL to prevent a dangling pointer
+
+ -- Kernel Engineer <kernel.engineer@canonical.com>  Wed, 15 Jan 2025 12:42:30 -0500
 
 linux-gke (6.8.0-1016.20) noble; urgency=medium
```

## Verify the kernel builds successfully

Now that our local `linux-gke` kernel source tree has been updated, we should test that it builds successfully.
We will be using our cloud builder system (CBD) for this purpose.

Connect to the Canonical VPN and run:

```bash
git remote add cbd cbd.kernel:noble.git
git push cbd
```

The output will initially look like this:

```{code-block}
:emphasize-lines: 4

Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
remote: *** kernel-cbd *********************************************************
remote: * Queueing builds (your 'cranky/master-next'); ok to interrupt
remote: * For results:  ssh cbd ls kernelengineer-noble-6c9a5055b22f-szkb
```

At this point you can interrupt the command with {kbd}`Ctrl-C` and periodically check the build status with the `ssh` command it printed. For example:

```bash
ssh cbd ls kernelengineer-noble-6c9a5055b22f-szkb
```

You should see the build progress for each architecture with either `BUILDING` or `BUILD-OK` status.

```{terminal}
:input: ssh cbd ls kernelengineer-noble-6c9a5055b22f-szkb
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main

2025-01-24 04:38:50          0 amd64/BUILDING
2025-01-24 04:38:51          0 arm64/BUILDING
```

For the `linux-gke` kernel, this shows us the builds are still in progress for the amd64 and arm64 architectures.

Once all the architectures return the `BUILD-OK` status, we know the kernel built successfully.

<!-- TODO: If we want to encourage external users to use cranky, what is the alternative for testing the builds here? -->

## Package the kernel for release - `cranky update-dependents`

To update all dependent packages in this `linux-gke` tree set (e.g. `linux-meta`, `linux-signed`, `linux-lrm`), run:

```bash
cranky update-dependents
```

If successful, you should see the "SUCCESS: update complete" message in the output.

### Tag commit - `cranky tags`

The last step is to tag your commit with the appropriate version tag.

```{caution}
Once a tag is pushed to the repository it cannot be modified.
So be sure to tag your commit only after verifying that your kernel source tree has been updated correctly and builds successfully.
```

```bash
cranky tags
```

You see should something similar returned in the terminal output:

```{terminal}
:input: cranky tags
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main

Tagging with:
 git tag -f -s -m Ubuntu-gke-6.8.0-1018.22 Ubuntu-gke-6.8.0-1018.22
```

### Verify preparation - `cranky verify-release-ready`

Perform one last sanity check on the git trees to screen out any issues with the kernel preparation by running:

```bash
cranky verify-release-ready
```

```{note}
The "tag pushed: warning" is an expected warning if you do not have commit rights.
```

### Pull sources

```bash
cd ..
# CWD == ~/canonical/kernel/noble/linux-gke/

cranky pull-sources noble:linux-gke --latest
```

### Build sources
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

This will generate several `.debdiff` files, which show the difference between this deb package and the last one.
You should review these files in a text editor (using a command like `vim *.debdiff`) to ensure there are no unexpected changes.
However, for the sake of this tutorial, we can assume the diffs are all correct.

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

## Related topics

Learn more about Ubuntu releases and derivative kernels [here].

<!-- LINKS -->

[VPN connection]: https://canonical-kteam-docs.readthedocs-hosted.com/en/latest/how-to/new_starter/newstarter.html#setup-vpn
[Kernel team build resources]: https://canonical-kteam-docs.readthedocs-hosted.com/en/latest/how-to/new_starter/newstarter.html#build-resources
