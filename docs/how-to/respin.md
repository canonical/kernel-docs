# How to respin a kernel

Sometimes regressions or last-minute changes are identified in kernels in #proposed (already cranked).

It is possible to make changes before the SRU cycle closes. This is a special version of a crank called a respin.

These are the steps to respin a kernel, with examples from a previous `2025.01.13` respin of the `noble:linux-gke` kernel due to a late-cycle decision to revert a patchset.

## 1. Create a respin Jira card

```{attention}
Only one person peforms this step. If you already have a Jira card, note the respin number in the card (see Note at the end of this step) and skip this step.
```

Use [kteam-tools create-respin-card](https://kernel.ubuntu.com/forgejo/kernel/kteam-tools/src/branch/master/stable/create-respin-card) script:

```text
./create-respin-card <cycle-number>
```

This will create a respin card on Jira. (For example, here's the one we created: [KSRU-15479 (Jira)](https://warthogs.atlassian.net/browse/KSRU-15479))

Next, on Jira, fill in the details of the respin in the description. This can include:

* Details on why the kernel is being respun
* Links to relevant bugs
* Affected kernels that will need to be respun

```{note}
Note the respin number, as it's used in subsequent steps.

The respin number is in the title of the Jira card in parentheses.
For example, "Re-spin (#8)" indicates the number is 8. 
```

## 2. Create tracking bugs
Each affected kernel needs a new Launchpad tracking bug.

Use the [kteam-tools/stable/create-kernel-tasks] script:

```text
./create-kernel-tasks --handle <handle> --spin <spin-number> <cycle-number>
```

For example, we used:
```{terminal}
:input: ./create-kernel-tasks --handle noble:linux-gke --spin 8 2025.01.13
:dir: kteam-tools/stable/
```

The output states that a new tracking bug has been made, prints its bug number, and also prints the bug number for the original tracking bug from this kernel's original crank.

On Launchpad, mark the original tracking bug as a duplicate of the newly-created bug.
<!-- TODO screenshots of how to do this -->

## 3. Checkout the last cranked version of the kernel

Use cranky to checkout the kernel:

```text
cranky checkout --cleanup --pristine <handle>
```

Then, use `cranky rmadison` to get the version number from the #proposed kernel:
```text
cranky rmadison <handle>
```

In `linux-main/`, ensure `HEAD` is on the tag of the kernel in #proposed (the output of `cranky rmadison`).

<!-- TODO what if it isn't (new commits were applied)? -->

<!-- For example, when running `git show` in `linux-main/`, we saw that `HEAD` was on `Ubuntu-` -->

## 4. Add patchset

```{attention}
This step only applies to kernels which don't have a parent with patches applied. If your kernel has a parent kernel where respin patches were applied, skip this step.
```

Usually patches will come from a mailing list, as `.patch` files. Use `git am` to apply them.

You may also be asked to modify the commit message.
<!--TODO elaborate?-->

## 5. Rebase
```{attention}
This step only applies to kernels which are derivatives of kernels also being respun. Skip this step if your kernel has a parent that isn't being respun.
```

Your kernel's parent will have a new tag from its respin. Rebase off that tag:
```text
cranky rebase -b <parent-respin-tag>
```

For `noble:linux-gke`, the parent kernel, `noble:linux`, was not respun, so we skipped this step.

## 6. Continue cranking, with some modifications

Run the following commands as normal:
```text
cranky open
cranky review-master-changes
```

In theory, no changes should be detected by this step.

Next, run `cranky link-tb` with a modified cycle number:
```text
cranky link-tb --sru-cycle <cycle-number>-<spin-number>
```

In our crank, we used `cranky link-tb --sru-cycle 2025.01.13-8`, where 8 was the spin number.

Next, run:
```text
cranky update-dkms-versions
```
In theory, no changes should be detected by this step.

Next, finish the crank:
```text
cranky close 
cranky update-dependents
cranky tags
```

## 7. Pull sources
The primary difference with pulling the previous deb package sources is that we need to specify to pull the ones in #proposed. (By default, `cranky pull-sources` pulls TODO.)

First, we need to know which versions are in #proposed. Run `cranky rmadison` to get this info:
```text
cranky rmadison <handle>
```

You can `grep` the result for "proposed", too.

Note both the package name `cranky rmadison` produces and the version numbers of each package this kernel has (main, meta, signed, etc.) that are in #proposed.

For each package, we will run `cranky pull-source`.

```{attention}
Note that the command is `cranky pull-source`, _not_ `cranky pull-sources` (no 's').
We use `cranky pull-source` on each package manually so that we can specify the correct version number for each one.
```

Then, use `cranky pull-source` with the following syntax:
```text
cd ..
cranky pull-source --no-verify <rmadison-package-name> <version-in-proposed> <series>
```

For example, the rmadison format looked like this (at time of our respin) for `noble:linux-gke`

```{terminal}
:input: cranky rmadison noble:linux-gke
:dir: noble/linux-gke/

 linux-gke        | 6.8.0-1003.5  | noble            | source 
 linux-gke        | 6.8.0-1017.21 | noble-security   | source 
 linux-gke        | 6.8.0-1017.21 | noble-updates    | source 
 linux-gke        | 6.8.0-1019.23 | noble-proposed   | source 
 linux-gke        | 6.8.0-1017.21 | noble-proposed#2 | source 
 linux-meta-gke   | 6.8.0-1003.5  | noble            | source 
 linux-meta-gke   | 6.8.0-1017.21 | noble-security   | source 
 linux-meta-gke   | 6.8.0-1017.21 | noble-updates    | source 
 linux-meta-gke   | 6.8.0-1019.23 | noble-proposed   | source 
 linux-meta-gke   | 6.8.0-1017.21 | noble-proposed#2 | source 
 linux-signed-gke | 6.8.0-1003.5  | noble            | source 
 linux-signed-gke | 6.8.0-1017.21 | noble-security   | source 
 linux-signed-gke | 6.8.0-1017.21 | noble-updates    | source 
 linux-signed-gke | 6.8.0-1019.23 | noble-proposed   | source 
 linux-signed-gke | 6.8.0-1017.21 | noble-proposed#2 | source
```

`noble:linux-gke` has `main`, `meta`, and `signed` packages, so we noted those specific package names and versions from `cranky rmadison`:

| package name | version in `noble-updates` |
| - | - |
| `linux-gke` | `6.8.0-1017.21` |
| `linux-meta-gke` | `6.8.0-1017.21` |
| `linux-signed-gke` | `6.8.0-1017.21` |

```{note}
In the example, the version numbers for each package are the same.
This is not always the case, so it's still important to go through this step for each package.
```

So, we ran the following commands:
```{terminal}
:input: cranky pull-source linux-gke 6.8.0-1017.21 noble
:dir: noble/linux-gke/
```

```{terminal}
:input: cranky pull-source linux-meta-gke 6.8.0-1017.21 noble
:dir: noble/linux-gke/
```

```{terminal}
:input: cranky pull-source linux-signed-gke 6.8.0-1017.21 noble
:dir: noble/linux-gke/
```

## 8. Build sources

We need to pass the information about the packages in #proposed gathered in the previous step (`pull-source`) to build the sources this time. 
<!--TODO why?-->

`cranky build-sources` has a `--build-opts` flag we can use to specify the version to use. Pass this flag once for each package, like so:

```bash
cd linux-main/
cranky build-sources --build-opts 'main:-v<version-in-updates>' --build-opts 'meta:-v<version-in-updates>' --build-opts 'signed:<version-in-updates>'
```

```{note}
The syntax used for each `--build-opts` is `<package-dirname>:-v<version>`.
The `package-dirname` is the name of the directory this package lives in (use `ls` to see them).
They are usually `linux-main/`, `linux-meta/`, `linux-lrm`, `linux-signed/`, etc.
Use these without the `linux-` prefix.
```

For example, we used the following command to build `noble:linux-gke`:

```{terminal}
:input: cranky build-sources --build-opts 'main:-v6.8.0-1017.21' --build-opts 'meta:-v6.8.0-1017.21' --build-opts 'signed:-v6.8.0-1017.21'
:dir: noble/linux-gke/linux-main
```

## 9. Review changes and upload

At this point, refer to the normal crank process to finish the respin.

```bash
cd ..
cranky review *.changes
```

Lastly, upload the package or push it for a peer-review.
