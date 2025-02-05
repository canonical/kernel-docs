# How to respin a kernel

Sometimes regressions or last-minute changes are identified in kernels in #proposed (already cranked).

It is possible to make changes before the SRU cycle closes. This is a special version of a crank called a respin.

These are the steps to respin a kernel, with examples from a previous respin of several Google kernels due to a late-cycle decision to revert a patchset.

## 1. Create a respin Jira card

```{note}
Only one person peforms this step. If you already have a Jira card, skip this step.
```

Use [kteam-tools/stable/create-respin-card](https://kernel.ubuntu.com/forgejo/kernel/kteam-tools/src/branch/master/stable/create-respin-card) script:

```text
create-respin-card [cycle-number]
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
create-kernel-tasks --handle <handle> --spin <spin-number> <cycle-number>
```

For example, we used:
```{terminal}
:input: create-kernel-tasks --handle noble:linux-gke --spin 8 2025.01.13
:dir: kteam-tools/stable/
```

The output states that a new tracking bug has been made, and also prints the bug number for the original tracking bug for this kernel's original crank.

On Launchpad, mark the original tracking bug as a duplicate of the newly-created bug:

<!-- TODO screenshots of how to do this -->

## 3. Checkout the last cranked version of the kernel

Use [cranky]() to checkout the kernel:

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

The following step depends on whether the kernel you are respinning has a parent kernel which itself is a derivative.

## 5. Continue cranking, with some modifications

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

<!-- TODO example -->

Next,
```text
cranky update-dkms-versions
```
In theory, no changes should be detected by this step.

Next,
```text
cranky close 
cranky update-dependents
cranky tags
```

Pulling and building the deb sources is pretty different:
TODO


