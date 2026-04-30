---
myst:
  html_meta:
    description: "Roll back a faulty kernel by reverting to an earlier version. Covers revert-kernels-to-spin and Archive Admin remove-package and copy-package commands."
---

# Kernel rollback

When a kernel is found to be so bad that the only option is to withdraw it from the archive, the typical approach is to replace it with the previous kernel.
This will not fix anything for those who have already upgraded their kernel, but can further prevent other {spellexception}`upgraders` becoming affected.

There have also been cases where upgrades are no longer possible with an update and reverting the update can restore the ability to upgrade.

This recipe will guide you through identifying the kernel versions to rollback to, and how to produce a recipe for a member of the Archive Admins (AA) to follow to perform the required rollback.

(ref-kernel-workflow-playbook-rollback-tooling)=

## Prerequisites

```{include} /reuse/kernel-workflow-playbook-tooling.txt
```

## Prepare (Kernel)

In order to revert the kernel in a pocket we need to identify an earlier version of a good kernel.
We typically identify this via a previous cycle or spin number, and handle.

We want to remove any existing kernel package publications for this handle, and then copy back earlier publications. 
Use the `revert-kernels-to-spin` command to generate AA commands to effectuate these:

```{code-block} shell
/revert-kernels-to-spin --spin s2025.09.15 --handle noble:linux \
        --pocket updates --reason "Causing upgrade issues" --yes
```

## Validation (Kernel)

The kernel team should review the versions that the revert is settled on, as shown in the revert output.
It is vital to confirm that any LRM or signed respins have been included.
Where there is a later version the tooling will emit a warning as below.
The versions should be updated manually in this case.

```{code-block} shell
# jammy:linux-azure: spin=s2025.10.13-2 full_versions={'lrm': '5.15.0-1102.111+1', 'main': '5.15.0-1102.111', 'meta': '5.15.0.1102.100', 'signed': '5.15.0-1102.111'}
[...]
# WARNING: linux-restricted-modules-azure looks to have a repin not in the spin (5.15.0-1102.111+1)
```

## Execute (Archive Admins)

In order to revert a kernel, all of the packages which make up a kernel (e.g. `linux`, `linux-signed`, `linux-meta`, `linux-restricted-modules` etc) must be reverted together.
The kernel team will identify these packages and the versions of which are faulty, and the older package versions which should be reinstated.
They will use {ref}`kernel tooling <ref-kernel-workflow-playbook-rollback-tooling>` to generate `remove-package` and `copy-package` commands to roll-back the published versions of these packages.

These will consist of two groups of commands: an initial set of removals, one per package, plus a second set of copies for the same packages.
While it is possible for the two sets to differ, additional consideration is necessary in this case.
For example:

```{code-block} shell
remove-package linux                       --version 6.8.0-88.89   --archive ubuntu --suite      noble-updates --removal-comment='Causing upgrade issues' -y
remove-package linux-meta                  --version 6.8.0-88.89   --archive ubuntu --suite      noble-updates --removal-comment='Causing upgrade issues' -y
remove-package linux-restricted-modules    --version 6.8.0-88.89+1 --archive ubuntu --suite      noble-updates --removal-comment='Causing upgrade issues' -y
remove-package linux-restricted-signatures --version 6.8.0-88.89+1 --archive ubuntu --suite      noble-updates --removal-comment='Causing upgrade issues' -y
remove-package linux-signed                --version 6.8.0-88.89   --archive ubuntu --suite      noble-updates --removal-comment='Causing upgrade issues' -y
copy-package   linux                       --version 6.8.0-87.88   --from    ubuntu --from-suite noble-updates --include-binaries --force-same-destination --auto-accept -y
copy-package   linux-meta                  --version 6.8.0-87.88   --from    ubuntu --from-suite noble-updates --include-binaries --force-same-destination --auto-accept -y
copy-package   linux-restricted-modules    --version 6.8.0-87.88+1 --from    ubuntu --from-suite noble-updates --include-binaries --force-same-destination --auto-accept -y
copy-package   linux-restricted-signatures --version 6.8.0-87.88+1 --from    ubuntu --from-suite noble-updates --include-binaries --force-same-destination --auto-accept -y
copy-package   linux-signed                --version 6.8.0-87.88   --from    ubuntu --from-suite noble-updates --include-binaries --force-same-destination --auto-accept -y
```

```{note}
If the `security` pocket is later than the newly rolled-back kernel version in `updates`, the same procedure should be applied to the `security` pocket.
```

## Execute (IS)

Where the affected series include those in ESM, removals from the primary PPAs the packages will also need removing from the {spellexception}`repropro` repository.
Take a list of the removed packages in the ESM series to mattermost \~IS channel, and request for them to be removed.

A sample removal command is shown below:

```shell
reprepro --basedir /srv/esm-archive/fips-updates/reprepro/ removesrc \
      focal-infra-security openssh '1:9.6p1-3ubuntu13.7+Fips1'
```

```{tip}
If you are unable to contact the Canonical IS team directly, liaise with a member of the Canonical Kernel team to request the removal of said packages.
```
