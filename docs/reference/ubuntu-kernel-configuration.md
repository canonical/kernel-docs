---
myst:
  html_meta:
    description: "Reference for Ubuntu kernel configuration: upstream Kconfig options, the config annotations format, architectures, flavours, and the generated .config files."
---

```{owners} rossporter506
```

(ref-ubuntu-kernel-configuration)=

# Ubuntu kernel configuration

Ubuntu maintains one kernel configuration per supported architecture and
{term}`flavour` for each kernel tree. Three layers produce that
configuration:

1. Upstream `Kconfig` files define the available options, their types,
   defaults, and dependencies.
1. Ubuntu config annotations in `debian.<kernel>/config/annotations` record
   the value Ubuntu requires for each option, per architecture and flavour.
1. At build time, the annotations are compiled into a `.config` for each
   architecture and flavour. The installed kernel ships its configuration as
   `/boot/config-<ver>-<flavour>` (for example,
   `/boot/config-6.8.0-147-generic`), so you can compare your changes against
   the configuration of a running Ubuntu kernel.

This page describes each layer and the tools used to manage them. If you only
want to change a configuration option and build a kernel,
{doc}`/how-to/develop-customise/build-kernel` covers the workflow end to end.

```{seealso}
{doc}`/reference/ubuntu-kernel-source-packaging` describes the source tree
that contains these files.
```

## Upstream Kconfig

Upstream `Kconfig` files throughout the source tree define the configuration
options. Most options are `bool` or `tristate`:

- `y` builds the feature into the kernel image.
- `m` builds the feature as a loadable module (tristate options only).
- `n` disables the feature.

Options can also take string, integer, or hexadecimal values. Dependencies
between options (`depends on`, `select`) mean that changing one option can
change or hide others.

The default Ubuntu policy is to enable features as modules where possible,
except for debugging, testing, or deprecated features. See
[Kernel configuration in Ubuntu] for background on this policy.

## Config annotations

Each Ubuntu kernel tree stores its configuration in
`debian.<kernel>/config/annotations`. A header defines the format version
and the supported architectures and flavours:

```{code-block} text
# Menu: HEADER
# FORMAT: 4
# ARCH: amd64 arm64 armhf ppc64el riscv64 s390x
# FLAVOUR: amd64-generic arm64-generic arm64-generic-64k armhf-generic ppc64el-generic riscv64-generic s390x-generic
```

Each entry sets the value of one option with `policy<>`, and can carry a
justification with `note<>`:

```{code-block} text
CONFIG_ARCH_MMAP_RND_BITS                     policy<{'amd64': '32', 'arm64': '33', 'arm64-generic-64k': '29', 'armhf': '16', 'ppc64el': '29', 'riscv64': '24'}>
CONFIG_ARCH_MMAP_RND_BITS                     note<'LP: #1983357'>
```

- The keys of `policy<>` are architectures or architecture-flavour pairs.
  A value of `-` means the option must not appear in the `.config` at all,
  usually because it does not exist on that architecture. This differs from
  `n`, which means the option exists and is disabled.
- The `note<>` records why the value is required, usually as a Launchpad bug
  reference or a short rationale.

The build checks every option in the generated `.config` against the
annotations and fails on any mismatch, whether or not the option has a note.
Options with notes are deliberate decisions that must be preserved across
rebases; the remaining options follow the default Ubuntu policy and are listed
in the "Annotations without notes" section of the file. The annotations format
version has evolved over time; format 4 is current.

## Configuration inheritance

A kernel that builds on another kernel's configuration includes that kernel's
annotations with an `include` line and lists only its overrides. A flavour of
the including kernel gets the included kernel's value for each option unless
it overrides it. Optionally, a `FLAVOUR_DEP` header line maps a flavour to
a parent flavour, so the flavour also gets values the parent sets for that
specific flavour rather than for the whole architecture. For example, the
header of the `linux-aws` tree for Jammy Jellyfish (22.04):

```{code-block} text
# Menu: HEADER
# FORMAT: 4
# ARCH: amd64 arm64
# FLAVOUR: amd64-aws arm64-aws arm64-aws-64k
# FLAVOUR_DEP: {'amd64-aws': 'amd64-generic', 'arm64-aws': 'arm64-generic', 'arm64-aws-64k': 'arm64-generic-64k'}

include "../../debian.master/config/annotations"
```

When resolving an option for a flavour, the tools use the first value found
for the `<arch>-<flavour>` key, then for the `FLAVOUR_DEP` parent flavour,
then for the `<arch>` key. Here, `arm64-aws-64k` therefore gets the values
set for `arm64-generic-64k`, such as its larger page size, rather than only
the values set for `arm64`.

See {doc}`/reference/ubuntu-kernels` for more on kernel flavours.

## Query and edit the annotations

The `debian/scripts/misc/annotations` script reads and writes the annotations
file. Run it from the top of the kernel source tree; it finds the annotations
file through `debian/debian.env`. Common operations:

```{code-block} shell
# Show the policy for one option across all architectures and flavours
./debian/scripts/misc/annotations --query --config CONFIG_DEBUG_INFO_BTF

# Export the .config for one architecture and flavour
./debian/scripts/misc/annotations --arch arm64 --flavour generic-64k --export > .config

# Import a full .config into the annotations
./debian/scripts/misc/annotations --arch amd64 --flavour generic --import .config
```

The script also supports `--update` to resynchronize a subset of options from
a partial `.config`, and `--check` to validate a `.config` against the
annotations. Run it with `--help` for the full list of actions.

## Configuration targets in debian/rules

The packaging exposes the configuration operations as `debian/rules` targets:

- `fakeroot debian/rules editconfigs` asks, for each architecture and
  flavour, whether to edit its configuration. It opens `menuconfig` for each
  one you accept, and writes the result back to the annotations.
  This is the recommended way to change the configuration; see
  {doc}`/how-to/develop-customise/build-kernel`.
- `fakeroot debian/rules updateconfigs` resynchronizes the annotations after
  options were added, removed, or renamed upstream, for example after a
  rebase or after importing a `.config`. It prompts for a value for each new
  option (`syncconfig`).
- `fakeroot debian/rules defaultconfigs` does the same without prompting,
  setting each new option to its upstream default (`olddefconfig`).
- `fakeroot debian/rules genconfigs` writes the generated `.config` files to
  `CONFIGS/` without changing the annotations.

These targets process every architecture listed in the annotations, so the
cross-compiler for each architecture must be installed. If one is missing,
that architecture is skipped and the target fails with
`Config operation not applied to all architectures`.

## Configuration in older kernel trees

Current kernel trees maintain the configuration entirely in annotations.
Older trees, such as the 4.4 and 4.15 kernels in Xenial Xerus (16.04) and
Bionic Beaver (18.04), store the configuration as Kconfig chunks under
`debian.<kernel>/config/` that are concatenated to form each `.config`:
options common to all architectures (`config.common.ubuntu`), options common
to one architecture (`<arch>/config.common.<arch>`), and options specific to
one flavour (`<arch>/config.flavour.<flavour>`). An annotations file in an older
format records only the options that must keep specific values. The
`annotations` script described on this page is not available in these trees.

The format depends on the kernel tree rather than the release: newer kernels
shipped to an older release, such as `linux-azure-5.4` in Bionic Beaver, use
annotations.

## Related topics

- {doc}`/reference/ubuntu-kernel-source-packaging`
- {doc}`/reference/ubuntu-kernels`
- {doc}`/how-to/develop-customise/build-kernel`
- {doc}`/how-to/develop-customise/build-kernel-snap`
- [Kernel configuration in Ubuntu]

% LINKS

[Kernel configuration in Ubuntu]: https://discourse.ubuntu.com/t/kernel-configuration-in-ubuntu/35857
