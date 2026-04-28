---
myst:
  html_meta:
    description: "Expedite an SRU kernel release to updates using copy-package-kernel. Learn the workflow for kernel team preparation and Archive Admin execution steps."
---

# Releasing an SRU kernel

If you need to expedite the release of a kernel build as part of the SRU cycle process but you are unable to get hold of a Kernel Archive Admin (AA), you can use the following recipe.

## Prepare (Kernel)

To release a kernel it must be in calling to be released via the `promote-to-updates` task. 
Liaise with the Kernel Stable team to get the testing and {spellexception}`signoffs` into an appropriate state to cause the tracker, a Launchpad bug against kernel-sru-workflow project, to ask to release.

We can then form a release command for the Archive Admins to execute.

```{code-block} shell
./copy-package-kernel --from-route proposed --to-route updates --tracker <tracker>
```

## Execute (Archive Admin)

Kernels are promoted using the `copy-package-kernel` command from [ubuntu-archive-tools].
This command makes use of the kernel-team databases to identify the source and destination for the copies.
It also has internal validation to confirm that the package collection in the destination pocket will be internally consistent by versions after the copies.

The kernel team will bring the bones of a `copy-package-kernel` command for the required promotion for execution. 

First, check that the tracker provided with the command is requesting to be released.
There should be a task against `promote-to-updates` which should be in "Confirmed" state.

- If this is _not_ the case, then this should be handed back to the kernel-team for resolution.
- If it is, assign that task to yourself, and move it to "In Progress".

The supplied command can be safely run with the `-n` argument to see what it would do; you can also add the `–verbose` option to dump out the equivalent `copy-package` kernel commands for validation.

```{terminal}
:user: user
:host: host

/copy-package-kernel --from-route proposed --to-route updates --tracker 2127318 -n --verbose

copy-tracker: 2127318 (focal:linux-iot) proposed updates
  Versions:   -final-        -was-
    main      5.4.0-1056.59  5.4.0-1055.58
    meta      5.4.0.1056.54  5.4.0.1055.53
    signed    5.4.0-1056.59  5.4.0-1055.58
  Copies:
    linux-iot                                     5.4.0-1056.59             ppa:canonical-kernel-esm/ubuntu/proposed:Release -> ppa:ubuntu-esm/ubuntu/esm-infra-security:Release ... dry-run
      copy-package -n --include-binaries --auto-approve \
        --from ppa:canonical-kernel-esm/ubuntu/proposed	 --from-suite focal \
        --to ppa:ubuntu-esm/ubuntu/esm-infra-security --to-suite focal \
        --version 5.4.0-1056.59 linux-iot
    linux-meta-iot                                5.4.0.1056.54             ppa:canonical-kernel-esm/ubuntu/proposed:Release -> ppa:ubuntu-esm/ubuntu/esm-infra-security:Release ... dry-run
      copy-package -n --include-binaries --auto-approve \
        --from ppa:canonical-kernel-esm/ubuntu/proposed --from-suite focal \
        --to ppa:ubuntu-esm/ubuntu/esm-infra-security --to-suite focal \
        --version 5.4.0.1056.54 linux-meta-iot
    linux-signed-iot                              5.4.0-1056.59             ppa:canonical-kernel-esm/ubuntu/proposed:Release -> ppa:ubuntu-esm/ubuntu/esm-infra-security:Release ... dry-run
      copy-package -n --include-binaries --auto-approve \
        --from ppa:canonical-kernel-esm/ubuntu/proposed --from-suite focal \
        --to ppa:ubuntu-esm/ubuntu/esm-infra-security --to-suite focal \
        --version 5.4.0-1056.59 linux-signed-iot
```

If you are happy with the output, rerun it with `-y` to execute it.
It is safe to run the command more than once as it is idempotent.
Running it a second time will confirm the copies have been accepted by Launchpad. 

When the copy completes external tooling should manage the state of `promote-to-updates` through to "Fix Released".

[ubuntu-archive-tools]: https://code.launchpad.net/ubuntu-archive-tools
