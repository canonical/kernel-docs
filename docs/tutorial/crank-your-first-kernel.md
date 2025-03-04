# Tutorial: Crank your first kernel

Cranking an Ubuntu kernel is the process of applying patches and updates to an existing Ubuntu kernel, packaging it, and preparing it for testing.
All this is done using the [cranky](https://kernel.ubuntu.com/gitea/kernel/kteam-tools/src/branch/master/cranky) toolchain.

In this tutorial, we will crank a 24.04 LTS (Noble Numbat) (codename `noble`) Google cloud kernel (codename `linux-gke`) from the "s2024.12.02" cycle.
This starts our kernel at version "6.8.0-1017.21", from which we will create a new version "6.8.0-1018.22".

```{tip}
 Keep these codenames and cycle name handy for future commands.
```

## Prerequisites

You will need to complete the prerequisite setup below before proceeding with the tutorial:

- {doc}`Set up your cranky environment </how-to/cranking/set-up-cranky-environment>`
- Set up your [VPN connection]
- Get access to [Kernel team build resources]

## Set up and update build environment

First, we will prepare our build environment and tooling needed for cranking a kernel.

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

## Download kernel sources - `cranky checkout`

You're now ready to clone the `linux-gke` kernel for the given cycle (e.g. "s2024.12.02").

```bash
cranky checkout noble:linux-gke --cycle s2024.12.02
```

This command can take several minutes to complete.

If the command completes successfully, you should see the following new directory: `~/canonical/kernel/ubuntu/noble/linux-gke/`.

Inside, there should be three git repositories cloned: `linux-main`,  `linux-meta`, and `linux-signed`.

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

### Rebase on top of parent kernel - `cranky rebase`

As `noble:linux-gke` is a derivative kernel, we need to apply updates from its parent, `noble:linux`.

Choose a tag from the parent kernel to rebase onto, and run:

```bash
cranky rebase -b Ubuntu-6.8.0-53.55
```

```{tip}
For non-derivative kernels (e.g., `noble:linux`), this step is not required.
```

You should observe something similar in the output terminal:

```{terminal}
:input: cranky rebase -b Ubuntu-6.8.0-53.55
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

Rebase still needed between Ubuntu-6.8.0-52.53 and Ubuntu-6.8.0-53.55.
II: record=/home/annecyh/canonical/kernel/ubuntu/noble/linux-gke/linux-main/.git/REBASE-SELECTOR
Successfully rebased and updated refs/heads/cranky/master-next-s2024.12.02.
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
:input: cranky open
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

[...]
/home/kernel-engineer/canonical/kteam-tools/cranky/cranky startnewrelease --commit
Creating new changelog set for 6.8.0-1018.22...
[cranky/master-next-s2024.12.02 911b0ad106e9] UBUNTU: Start new release
 1 file changed, 8 insertions(+)


***** Now please inspect the commit before pushing *****
```

Run `git show` to verify that this new commit starts with "UBUNTU: Start new release" and shows an update to {file}`./debian.gke/changelog`.

```{terminal}
:input: git show
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

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
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

Listing changes in "debian.master/" since 9f8080a647a9e2c8c9a52b3e471b3f22d4dc0c67...

f31315007228 UBUNTU: [Packaging] debian.master/dkms-versions -- update from kernel-versions (main/2025.01.13)
3a8a3b4039e7 UBUNTU: [Packaging] do not attempt to generate BTF header on armhf
59e4c08ecd84 UBUNTU: Upstream stable to v6.6.55, v6.10.14
fadfbbcc2798 UBUNTU: [Config] updateconfigs for MICROSOFT_MANA
b5bd2549a589 UBUNTU: [Config] updateconfigs for deprecated CONFIG_Z3FOLD
1878fd662392 UBUNTU: [Config] updateconfigs to set ILLEGAL_POINTER_VALUE for riscv64
267522e21042 UBUNTU: [Config] updateconfigs to select PROC_MEM_ALWAYS_FORCE
366c11c3240e UBUNTU: [Packaging] Add list of used source files to buildinfo package
6b86533cc3d1 UBUNTU: [Packaging] Sort build dependencies alphabetically
52051394e234 UBUNTU: Upstream stable to v6.6.54, v6.10.13
763dd57e5520 UBUNTU: [Config] update configs for CONFIG_CRYPTO_AES_GCM_P10
db4045cf4e9a UBUNTU: Upstream stable to v6.6.53, v6.10.12
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
cranky link-tb --sru-cycle s2024.12.02 --dry-run
```

```{tip}
If you are running `cranky link-tb` for the first time, you will be directed to the "Authorize application to access Launchpad on your behalf" page.
Choose your preferred option before continuing.
```

This step should update the Launchpad tracking bug -- which, among other things, will be used as an input for subsequent steps -- and create a git commit.

But since we used the `--dry-run` option for this tutorial, no changes are made to the local tree and no commit is created.

```{terminal}
:input: cranky link-tb --sru-cycle s2024.12.02 --dry-run
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

(This is a dry-run)
LP: #2097956 (noble/linux-gke: <version to be filled> -proposed tracker) s2024.12.02-1
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
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

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
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:input: cranky close
:user: kernel-engineer
:host: ubuntu-machine
:scroll:

[...]

* Run config-check for arm64-gke ...
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
git commit -m "UBUNTU [Config] gke: Update configs from 6.8.0-53.55" -m "Ignore: yes" -s
```

Finally, re-run `cranky close`.

```bash
cranky close
```

If successful, you should see a new commit when you run `git show`:

```diff
commit 6c9a5055b22f4c30aa3ba0c9df306762edb29197 (HEAD -> cranky/master-next-s2024.12.02)
Author: Kernel Engineer <kernel.engineer@canonical.com>
Date:   Wed Feb 12 13:49:40 2025 +0800

    UBUNTU: Ubuntu-gke-6.8.0-1018.22
    
    Signed-off-by: Kernel Engineer <kernel.engineer@canonical.com>

diff --git a/debian.gke/changelog b/debian.gke/changelog
index fd056a9e15cc..fd8c8d9cd8fb 100644
--- a/debian.gke/changelog
+++ b/debian.gke/changelog
@@ -1,10 +1,1229 @@
-linux-gke (6.8.0-1018.22) UNRELEASED; urgency=medium
+linux-gke (6.8.0-1018.22) noble; urgency=medium
 
-  CHANGELOG: Do not edit directly. Autogenerated at release.
-  CHANGELOG: Use the printchanges target to see the curent changes.
-  CHANGELOG: Use the insertchanges target to create the final log.
+  [ Ubuntu: 6.8.0-53.55 ]
 
- -- Kernel Engineer <kernel.engineer@canonical.com>  Wed, 12 Feb 2025 12:43:08 +0800
+  * noble/linux: 6.8.0-53.55 -proposed tracker (LP: #2093677)
+  * Packaging resync (LP: #1786013)
+    - [Packaging] debian.master/dkms-versions -- update from kernel-versions
+      (main/2025.01.13)
[...]

+ -- Kernel Engineer <kernel.engineer@canonical.com>  Wed, 12 Feb 2025 13:49:40 +0800
 
 linux-gke (6.8.0-1017.21) noble; urgency=medium
```

### Verify the kernel builds successfully

Now that our local `linux-gke` kernel source tree has been updated, we should test that it builds successfully.

<!--
### Build kernel in CBD
-->
For Canonical users, we can use the cloud builder system (CBD) for this purpose.

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
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

2025-01-24 04:38:50          0 amd64/BUILDING
2025-01-24 04:38:51          0 arm64/BUILDING
```

For the `linux-gke` kernel, this shows us the builds are still in progress for the amd64 and arm64 architectures.

Once all the architectures return the `BUILD-OK` status, we know the kernel built successfully.

<!--
### Build kernel locally

Since we have the chroot environment set up already, we can choose to build the kernel locally.

First, install additional dependencies:

```bash
cranky chroot run -u root noble:linux-gke -- apt install -y fakeroot llvm libncurses-dev dwarves
```

Clean up any temporary build files and reset the source tree:

```bash
cranky chroot run noble:linux-gke -- fakeroot debian/rules clean
```

Then build and compile the different kernel packages:

```bash
cranky chroot run noble:linux-gke -- fakeroot debian/rules binary-headers binary-generic binary-perarch
```

If the build is successful, you should find several .deb binary package files in the directory above the build root directory.

```{terminal}
:input: ls ../
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

TBD
```
-->

## Package the kernel for release - `cranky update-dependents`

To update all dependent packages in this `linux-gke` tree set (e.g. `linux-meta`, `linux-signed`, `linux-lrm`), run:

```bash
cranky update-dependents
```

If successful, you should see the "SUCCESS: update complete" message in the output.

## Final stages of kernel preparation

We are now in the final stages of preparing the kernel source before it can be uploaded.

### Tag commit - `cranky tags`

Tag your commit with the appropriate version tag.

```{caution}
Only tag your commit after verifying that your kernel source tree has been updated correctly and builds successfully.
Once a tag is pushed to the repository it cannot be modified.
```

```bash
cranky tags -f
```

You see should something similar returned in the terminal output since we are overriding existing tags with the `-f` option:

```{terminal}
:input: cranky tags -f
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

error: Tag 'Ubuntu-gke-6.8.0-1018.22' exists already
(--force specified - continuing anyway)
Tagging with:
 git tag -f -s -m Ubuntu-gke-6.8.0-1018.22 Ubuntu-gke-6.8.0-1018.22
Updated tag 'Ubuntu-gke-6.8.0-1018.22' (was eab9e1e8fc09)
error: Tag 'Ubuntu-gke-6.8.0-1018.22' exists already
(--force specified - continuing anyway)
Tagging with:
 git tag -f -s -m Ubuntu-gke-6.8.0-1018.22 Ubuntu-gke-6.8.0-1018.22
Updated tag 'Ubuntu-gke-6.8.0-1018.22' (was 961465c)
error: Tag 'Ubuntu-gke-6.8.0-1018.22' exists already
(--force specified - continuing anyway)
Tagging with:
 git tag -f -s -m Ubuntu-gke-6.8.0-1018.22 Ubuntu-gke-6.8.0-1018.22
Updated tag 'Ubuntu-gke-6.8.0-1018.22' (was 49ebbe9)
```

### Verify preparation - `cranky verify-release-ready`

Perform one last sanity check on the git trees to screen out any issues with the kernel preparation by running:

```bash
cranky verify-release-ready
```

The results for the sanity check should look similar to the output below:

```{terminal}
:input: cranky verify-release-ready
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:scroll:

linux-main:
                                           is valid git repo: pass
                                             release (noble): pass
                                         package (linux-gke): pass
                                     version (6.8.0-1018.22): pass
                                             ABI bump (1018): pass
                                           build number (22): pass
                                      closing release commit: pass
                      correct tag (Ubuntu-gke-6.8.0-1018.22): pass
                                                  tag pushed: pass
                                                  tag signed: warning
                        conformant release tracking bug line: pass
                                        release tracking bug: pass
                                 unique release tracking bug: fail
                                  no "Miscellaneous" entries: pass
                                        No tracker bug found: warning
                                   changelog commits subject: pass
                                        final commit content: pass
linux-meta:
                                           is valid git repo: pass
                                           build number (22): pass
                                      closing release commit: pass
                      correct tag (Ubuntu-gke-6.8.0-1018.22): pass
                                                  tag pushed: pass
                                                  tag signed: warning
                                        final commit content: pass
linux-signed:
                                           is valid git repo: pass
                                           build number (22): pass
                                      closing release commit: pass
                      correct tag (Ubuntu-gke-6.8.0-1018.22): pass
                                                  tag pushed: pass
                                                  tag signed: warning
                                        final commit content: pass
```

The "tag pushed: pass" status is based on the tag for this version that was previously pushed when it was cranked.
The "unique release tracking bug: fail" status is expected since we did not link a new tracking bug in this tutorial.

### Pull sources - `cranky pull-source`

The final step of preparing the package update is building the source packages that need to be uploaded.

First, we will need to pull in the changes of the previous kernel version (`6.8.0-1017.21`) that we want to base our current kernel version off of.
This is required for the main and dependent packages.

```bash
cd ~/canonical/kernel/noble/linux-gke/
cranky pull-source linux-gke '6.8.0-1017.21'
cranky pull-source linux-signed-gke '6.8.0-1017.21'
cranky pull-source linux-meta-gke '6.8.0-1017.21'
```

If successful, you should have these files in the {file}`linux-gke` directory.

```{terminal}
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke
:input: ls *6.8.0-1017.21*
:scroll:

linux-gke_6.8.0-1017.21.diff.gz
linux-gke_6.8.0-1017.21.dsc
linux-meta-gke_6.8.0-1017.21.dsc
linux-meta-gke_6.8.0-1017.21.tar.xz
linux-signed-gke_6.8.0-1017.21.dsc
linux-signed-gke_6.8.0-1017.21.tar.xz
```

### Build sources - `cranky build-sources`

Build the source packages for your updated `linux-gke` source tree.

```bash
cd linux-main/
cranky build-sources
```

Check that you have the following artefacts in the {file}`linux-gke` directory:

```{terminal}
:user: kernel-engineer
:host: ubuntu-machine
:dir: ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main (cranky/master-next-s2024.12.02)
:input: cd ../ && ls *6.8.0-1018.22*
:scroll:

linux-gke_6.8.0-1018.22.diff.gz
linux-gke_6.8.0-1018.22.dsc
linux-gke_6.8.0-1018.22_source.buildinfo
linux-gke_6.8.0-1018.22_source.changes
linux-meta-gke_6.8.0-1018.22.dsc
linux-meta-gke_6.8.0-1018.22.tar.xz
linux-meta-gke_6.8.0-1018.22_source.buildinfo
linux-meta-gke_6.8.0-1018.22_source.changes
linux-signed-gke_6.8.0-1018.22.dsc
linux-signed-gke_6.8.0-1018.22.tar.xz
linux-signed-gke_6.8.0-1018.22_source.buildinfo
linux-signed-gke_6.8.0-1018.22_source.changes
```

## Review changelog - `cranky review`

We are now ready to review all the changes and updates that have been made for your `linux-gke` kernel.

```bash
cd ~/canonical/kernel/ubuntu/noble/linux-gke/
cranky review *.changes
```

This will generate 3 {file}`*.debdiff` files, each showing the difference between the latest deb package and the previous one.
These source changes should be reviewed in a text editor (e.g. using a command like `vim *.debdiff`) to ensure there are no unexpected changes.

## Upload

Normally, at this point a cranker with upload rights would publish the newly-cranked kernel to its PPA, which automatically kicks off boot testing.
However, without upload rights, we can request someone with rights to review our work, and publish the kernel on our behalf.

To push the created files to a server that is accessible to the reviewer (e.g. like `kathleen`):

```bash
cd linux-main/
cranky push-review -s s2024.12.02 kathleen
```

## Related topics

- [Ubuntu kernel variants]
- {doc}`/explanation/stable-release-updates`


<!-- LINKS -->

[VPN connection]: https://canonical-kteam-docs.readthedocs-hosted.com/en/latest/how-to/new_starter/newstarter.html#setup-vpn
[Kernel team build resources]: https://canonical-kteam-docs.readthedocs-hosted.com/en/latest/how-to/new_starter/newstarter.html#build-resources
[Kernel SRU dashboard]: https://kernel.ubuntu.com/reports/kernel-stable-board/
[Ubuntu kernel variants]: https://ubuntu.com/kernel/variants
