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

### Update chroot environment

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

## Download current version of kernel

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

### Fix helper scripts

Update the local (in-tree) helper scripts cranky uses to the latest version:

```bash
cd ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main/
cranky fix
```

You should see that cranky executed several scripts and go through the updating process for various scripts in the output terminal.

### Rebase on top of updated parent

As `linux-gke` is a derivative kernel, we need to apply updates from its parent, the generic kernel:

```bash
cranky rebase
```

```{tip}
For non-derivative kernels (e.g., `noble:linux`), this step is not required.
```

### Fix helper scripts (again)

Sometimes after a `cranky rebase`, the helper scripts get updated.
It's good practice to always re-run:

```bash
cranky fix
```

## Commit and review updates

Now that we've pulled in all the upstream changes, we are ready to review and apply the commits to the `linux-gke` kernel.

### Add starting commit

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

### Review rebased changes

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

For the purposes of this tutorial, no additional commits need to be added.

### Link to Launchpad bug tracker

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

### Update DKMS packages

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

### Add closing commit

We will now create one final commit before preparing a release by running:

```bash
cranky close
```

This command is a shortcut that does the following:

<!-- FEEDBACK: changelog? specifying the file path would help -->
1. Verifies there are no changes left. <!-- TODO elaborate? -->
2. Inserts changes from the parent kernel (`noble:linux`) into the debian changelog.
3. Inserts git changes into the changelog.
4. Updates the release series, author and date on the changelog, thus closing the changelog.
5. Creates a commit signifying the finished crank.

<!-- FEEDBACK: I think we need to add a step that says it is expected to fail since cranky review-master-changes has a bunch of commits related to config changes. So this step will fail initially until you commit the file. -->
<!-- FEEDBACK: https://canonical-kteam-docs.readthedocs-hosted.com/en/latest/tutorial/cranky_tutorial.html#close-the-changelog-cranky-close it's mentioned here but it isn't obvious -->

`cranky close` should fail, stating that there were changes in `debian.gke/config/annotations`. (If it didn't, move on to the next step.)
In this particular crank, we need to manually review and commit these changes:
```
git add debian.gke/config/annotations
git commit -m "UBUNTU [Config] gke: Update CONFIG_NVME_KEYRING"
```
The commit message is a simple description of the updated config.

Finally, re-run `cranky close`.
If successful, you should see a new commit when you run `git show`:

```diff
commit 6c9a5055b22f4c30aa3ba0c9df306762edb29197 (HEAD -> cranky/master-next)
Author: Benjamin Wheeler <benjamin.wheeler@canonical.com>
Date:   Wed Jan 15 12:42:31 2025 -0500

    UBUNTU: Ubuntu-gke-6.8.0-1017.21
    
    Signed-off-by: Benjamin Wheeler <benjamin.wheeler@canonical.com>

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
 
- -- Benjamin Wheeler <benjamin.wheeler@canonical.com>  Wed, 15 Jan 2025 12:04:33 -0500
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
+ -- Benjamin Wheeler <benjamin.wheeler@canonical.com>  Wed, 15 Jan 2025 12:42:30 -0500
 
 linux-gke (6.8.0-1016.20) noble; urgency=medium
```

## Verify the kernel builds successfully

At this point, the kernel is built and packaged. We should test that it builds successfully.

<!-- TODO verify above statement! -->

### Cloud Builder 

Connect to the canonical VPN. Then, run:

```bash
git remote add cbd cbd.kernel:noble.git
git push cbd
```

The output will initially look like this:
```
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
remote: *** kernel-cbd *********************************************************
remote: * Queueing builds (your 'cranky/master-next'); ok to interrupt
remote: * For results:  ssh cbd ls benjaminwheeler-noble-6c9a5055b22f-szkb
```

At this point you can interrupt the command with Ctrl-C and periodically check the build status with the ssh command it printed.

When running it, you'll see a few files either called `BUILDING` or `BUILD-OK`.

Once all the arches have `BUILD-OK`, we know the kernel built successfully.


<!-- TODO ask others about alternatives to CBD/kathleen. Those are for canonicalers only. Is it possible/easy to test in a way that anyone can do? -->

## Package the kernel for release
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

### Verify preparation
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
