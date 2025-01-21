# Tutorial: Crank your first kernel

Cranking an Ubuntu kernel is the process of applying patches and updates to an existing Ubuntu kernel, packaging it, and preparing it for testing. All this done using the [cranky](https://kernel.ubuntu.com/gitea/kernel/kteam-tools/src/branch/master/cranky) toolchain.

<!-- TODO specify the SRU cycle -->
In this tutorial, we will crank a 24.04 LTS (Noble Numbat) (codename `noble`) Google cloud kernel (codename `linux-gke`). Keep these codenames in mind for future commands.

## Set up and update build environment

<!-- TODO add cranky setup how-to -->
You will need to complete the setup according to the {doc}`cranky environment setup </how-to/cranking/set-up-cranky-environment>` guide before continuing.

### Update chroot environment

We use [chroot](https://en.wikipedia.org/wiki/Chroot) environments to isolate different sets of tools when doing kernel cranking. `cranky` helps us set up and manage these chroot jails.

<!-- FEEDBACK: it isn't obvious which part is specific to the "first time setup". Meaning if this is NOT the first time you're working on it, does it mean you skip this particular create-base step or skip the whole section? Maybe add "if not, skip create-base step", along those lines. -->
If this is your first time creating a chroot for the Noble Numbat release, you must first create the chroot base:

<!-- FEEDBACK: It seems like you MUST run this command from the ~ directory? If yes i guess it should be mentioned somewhere -->
```bash
cranky chroot create-base noble:linux-gke
```

This can take up to 20 minutes to complete.
If successful, you should observe the various packages being installed and set up in the terminal output.

Next, create the chroot session:

```bash
cranky chroot create-session noble:linux-gke
```

This step uses APT to install various packages needed for the crank and takes about two minutes to complete.

### Update kteam-tools repository

Update your local clone of `kteam-tools` to the latest commit on the `master` branch:
For the scope of this tutorial, we will use a particular version of cranky. Run the following commands to get it:

<!-- FEEDBACK: I think maybe stick to the `master` branch. I read through the discussion on Rake and i guess it makes sense for the `master` version to always work so it can be referenced. If it breaks then it's good for the tutorial to catch it also. -->

```{warning}
If your kteam-tools tree isn't clean, be sure to save your work before running the commands. 
They will modify the repository!
Git should warn you if any destructive actions might occur.
```

```bash
cd ~/canonical/kteam-tools/
git pull
git checkout cranky-tutorial
```
<!--TODO checkout a `cranky-tutorial` git tag instead to ensure it's the same-->

After `checkout`, you should see output similar similar to this:

:::{terminal}
    :input: git checkout cranky-tutorial
    :dir: ~/canonical/kteam-tools/
    :user: user
    :host: host
Note: switching to 'cranky-tutorial'.

...

HEAD is now at de4674e4 mainline-build/cod-update-virgin: Split script and update freedesktop repos
:::

## Download current version of kernel

You're now ready to clone the `linux-gke` kernel in its current state.

<!-- TODO is the cd required? Or does cranky checkout default to this dir? -->
<!-- TODO this probably needs SRU cycles specified so it's more reproducible. -->


<!-- FEEDBACK: I think this is missing a step as the directory shows up out of nowhere. a mkdir is needed i think for ~/canonical/kernel/ubuntu/ -->
```bash
cd ~/canonical/kernel/ubuntu/
cranky checkout noble:linux-gke
```

<!-- FEEDBACK: Could you restructure the sentences here similar to the previous paragraph? Which have command + expected output + expected completion time -->

Once this command is finished (It took ~20 minutes to complete), you should see the following directories inside the newly-created `./noble/linux-gke/` directory:
- `linux-main`: The actual Linux kernel source.
- `linux-meta`: Stores a set of meta-packages for the kernel. See {term}`linux-meta` for more information.
- `linux-signed`: Kernel packages that are cryptographically signed to ensure their integrity and authenticity. See {term}`linux-signed` for more information.

<!-- FEEDBACK: This is why we have glossary terms! We can link to it. -->

## Apply updates from upstream kernel

The upstream kernel will possibly have changes that should be propagated down to this kernel.

### Fix helper scripts

Update the local (in-tree) helper scripts cranky uses to the latest version:

```bash
cd ~/canonical/kernel/ubuntu/noble/linux-gke/linux-main/
cranky fix
```
You should see some output showing that cranky executed several scripts.
You see observe cranky going through the updating process for various scripts in the output terminal.

### Rebase on top of updated parent

As `linux-gke` is a derivative kernel, we need to apply updates from its parent, the generic kernel:

```bash
cranky rebase
```

<!-- FEEDBACK: is it likely for someone going through this step to encounter rebase failures? -->

```{tip}
For non-derivative kernels (e.g., `noble:linux`), this step is not required.
```

### Fix helper scripts (again)

Sometimes after a `cranky rebase`, the helper scripts get updated. It's good practice to always re-run:

```bash
cranky fix
```

<!-- TODO what should this section be called? -->
## Commit and review updates

Now that we've pulled in all the upstream changes, we are ready to review and apply the commits to the `linux-gke` kernel.

### Add starting commit

<!-- TODO this section doesn't really explain why we are doing these things. Learn what's going on and then document better. -->
<!-- FEEDBACK: we need minimal explanation for a tutorial. But if anything more is needed it can be added into a 'reference' for cranky which would be more detailed. And would the --help output from cranky be useful to help document this step? -->

Create a commit that signifies the start of a new release. This new commit will contain {term}`ABI` changes and any customization required by backport kernels.

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
    Signed-off-by: annecyh <anne.chew@canonical.com>

diff --git a/debian.gke/changelog b/debian.gke/changelog
[...]
```

### Review rebased changes

Sometimes the rebase doesn't get all the changes. So we need to run this command to manually review any outstanding changes:

```bash
cranky review-master-changes
```
This command will output any outstanding changes in a list with their commit hashes and descriptions. Use `git show <commit-hash>` to view the changes.

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

<!-- FEEDBACK: In a tutorial these shouldn't be necessary. A more generic how-to should contain all these instead. For the tutorial, the author should be aware of what changes are outstanding and expected in this list. -->

Usually these can be ignored, but there are a few instances where further investigation is necessary:

- Commits with changes to `debian.master/rules.d/`
    - Choose if these changes should be reflected in `debian.gke/rules.d/`
- Commits with descriptions starting with "UBUNTU: \[Config\]: ..."
    - These indicate a change in the parent kernel's configuration.
    - You'll need to compare this change with what appears in the derivative config (`debian.gke/`) to decide if it should be applied to this crank.

### Link to Launchpad bug tracker

Run the following command to link this kernel to its corresponding Launchpad bug tracker:
<!-- TODO "what" are we linking? This kernel? This crank? This repo? What's the proper word to use? -->
<!-- FEEDBACK: good point. some brief context would be helpful here. -->

```{warning}
Use `--dry-run` unless you are actually cranking a kernel. Otherwise, this will overwrite Launchpad and might make destructive changes!
```

```bash
cranky link-tb --dry-run
```

```{tip}
If you are running `cranky link-tb` for the first time, you will be directed to the "Authorize application to access Launchpad on your behalf" page. Choose your preferred option before continuing.
```

This step should update the Launchpad tracking bug -- which, among other things, will be used as an input for subsequent steps -- and create a git commit.

But since we used the `--dry-run` option for this tutorial, no changes are made to the local tree and no commit is created.

<!-- TODO when is the earliest/latest this step can be done? Is this ordering the most sensible? -->
<!-- FEEDBACK: I believe we should be skipping this step to run `git show` since no commit happens for a dry run. This can be kept in a how-to -->

### Update DKMS packages

The `debian.master/dkms-versions` file specifies dkms modules to be packaged with its kernel. This command updates the package versions in `debian.gke/dkms-versions` to match the ones expected for the <which> SRU cycle.
<!-- FEEDBACK: which SRU cycle are we referring to here? -->

```bash
cranky update-dkms-versions
```

Since changes are needed at this time, you should observe the following output:

```
debian.gke/dkms-versions: No changes from kernel-versions
```

In most cases there would be no change committed as the up-to-date versions should have been committed on the master kernel and picked-up by the derivative or backport on rebase. However, if there is any change, check that the version numbers only become higher and nothing gets dropped completely. In case anything looks suspicious, don’t hesitate to ask the team if the changes are expected.


### 4.5. Closing commit
This step creates one final commit before a release is prepared. Run:
```bash
cranky close
```
This command is a shortcut for several steps:

1. Verifies there are no changes left. <!-- TODO elaborate? -->
2. Inserts changes from the parent kernel into the changelog.
3. Inserts git changes into the changelog.
4. Updates the release series, author and date on the changelog, thus closing the changelog.
5. Creates a commit signifying the finished crank.

If the output went well, you should see a new commit when you run `git show`:
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

## 5. Verify the Kernel Builds Successfully
At this point, the kernel is built and packaged. We should test that it builds successfully.
<!-- TODO verify above statement! -->
### Cloud Builder 
<!-- TODO WARNING: cbd is internal only (?) What should we put here instead? -->

Connect to the canonical VPN. Then, run:
<!-- Add to prerequisites: VPN set up! -->

<!-- TODO add git remote add cbd -->


```bash
git push cbd
```

<!-- TODO describe output -->
<!-- TODO describe ssh -->

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

## 6. Package the kernel for Release
Run the following command:
<!--TODO add note that it's "dependents", not "dependent". -->
```bash
cranky update-dependents
```

### 6.1. Tag commit
```bash
cranky tags
```
<!-- TODO describe output -->

### 6.2. Verify Preparation
```bash
cranky verify-release-ready
```

The `tag pushed: warning` is an expected warning if you do not have commit rights.

### 6.3. Pull sources

```bash
cd ..
# CWD == ~/canonical/kernel/noble/linux-gke/

cranky pull-sources noble:linux-gke --latest
```

### 6.4. Build Sources
```bash
cd linux-main/
cranky build-sources
```

## 7. Review
```bash
cd ..
# CWD == ~/canonical/kernel/noble/linux-gke/
cranky review *.changes
```

## 8. Upload

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
