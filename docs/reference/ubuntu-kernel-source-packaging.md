---
myst:
  html_meta:
    description: "Reference for the Ubuntu kernel source tree: the debian/ and debian.<kernel>/ packaging directories, changelogs, version and ABI numbers, and generated files."
---

```{owners} rossporter506
```

(ref-ubuntu-kernel-source-packaging)=

# Ubuntu kernel source tree and packaging

An Ubuntu kernel source tree is the upstream Linux kernel source plus the
Ubuntu packaging, configuration, and patches needed to build the Ubuntu kernel
packages. This page describes the layout of the tree and the purpose of the
Ubuntu-specific files in it.

Each kernel tree keeps the packaging data specific to it in a
`debian.<kernel>/` directory; in the generic kernel tree this is
`debian.master/`. If you want to build a kernel, the files you are most likely
to work with are `debian.<kernel>/changelog`, which sets the package version, and
`debian.<kernel>/config/`, which holds the kernel configuration.
The rest of the packaging exists to turn the source into installable packages.

The examples on this page use the generic `linux` tree for Noble Numbat
(24.04 LTS). Other releases and kernel trees follow the same pattern, but
individual files and directories can differ between trees.

```{seealso}
- {doc}`/reference/ubuntu-kernel-configuration` describes the kernel
  configuration stored in these trees.
- {doc}`/explanation/ubuntu-kernel-patch-life-cycle` explains how patches
  move between upstream and Ubuntu.
- {doc}`/reference/ubuntu-kernels` describes the kernels and flavours Ubuntu
  provides.
```

## Source tree layout

Most of the tree (`arch/`, `drivers/`, `fs/`, `kernel/`, `mm/`, `net/`, and
the other top-level directories) is upstream Linux source. Ubuntu adds the
following directories:

| Path | Contents |
| ---- | -------- |
| `debian/` | Packaging machinery shared by every Ubuntu kernel tree: build rules, helper scripts, and package templates. |
| `debian.<kernel>/` | Data specific to one kernel tree: changelog, configuration, control templates, and per-architecture build rules. The generic kernel uses `debian.master/`; other kernels use their own directory, for example `debian.azure/` or `debian.xilinx/`. |
| `ubuntu/` | Ubuntu-specific drivers that are not upstream. Rarely used for new code. |

Ubuntu carries a small set of patches that are not upstream ({term}`SAUCE`
patches, cherry-picks, and backports). These patches modify the ordinary
upstream directories, so the difference from mainline is not limited to the
Ubuntu-specific directories. {doc}`/reference/stable-patch-format` defines
the `UBUNTU:` subject prefixes that identify each kind of change.

## The `debian/` directory

The `debian/` directory contains the packaging machinery common to all Ubuntu
kernel trees. `debian/rules` is the entry point for every package build.

| Path | Purpose |
| ---- | ------- |
| `debian/rules` | Makefile that implements the package build targets, such as `clean`, `binary`, and `editconfigs`. It includes the makefiles in `debian/rules.d/` and `debian.<kernel>/rules.d/`, and reads `debian/debian.env` to find the `debian.<kernel>/` directory. |
| `debian/rules.d/` | Makefiles included by `debian/rules`. They parse the version from the changelog, build the binary packages, and run checks during the build. |
| `debian/scripts/` and `debian/scripts/misc/` | Helper scripts used by the build, including the `annotations` script and the `kernelconfig` script behind the `editconfigs` target. |
| `debian/control.d/` | Package templates shared by all kernel trees: templates repeated for each {term}`flavour`, such as `linux-buildinfo`, and stubs for packages built only from the main `linux` package, such as `linux-source` and `linux-libc-dev`. |
| `debian/certs/` and `debian/revoked-certs/` | Certificates built into the kernel. `certs/` holds keys the kernel trusts, for example the Livepatch and ubuntu-drivers signing keys; `revoked-certs/` holds keys the kernel must reject. The build combines them into `debian/canonical-certs.pem` and `debian/canonical-revoked-certs.pem`. Modules are signed with a separate key generated during each build. |
| `debian/templates/` | Templates for the scripts that run when a kernel package is installed or removed. |
| `debian/debian.env` | Sets `DEBIAN` to the `debian.<kernel>/` directory for this tree, for example `DEBIAN=debian.master` or `DEBIAN=debian.azure`. |

## The `debian.<kernel>/` directory

Each kernel source package has its own `debian.<kernel>/` directory, which
holds the data specific to that kernel: `debian.master/` for `linux`,
`debian.azure/` for `linux-azure`, and so on. The name does not always match
the package name exactly, so use the `DEBIAN` setting in `debian/debian.env`
to find the directory a tree uses. All flavours built from the same source
package share the directory: `generic` and `generic-64k` both use
`debian.master/`, for example.

| Path | Purpose |
| ---- | ------- |
| `debian.<kernel>/changelog` | Changelog for the source package. The top entry sets the package version, target release, and {term}`ABI` number. The build copies it to `debian/changelog`. |
| `debian.<kernel>/config/` | Kernel configuration for the tree. See {doc}`/reference/ubuntu-kernel-configuration`. |
| `debian.<kernel>/control.stub.in` | Template for the build dependencies and flavour-independent packages in `debian/control`. |
| `debian.<kernel>/control.d/` | Per-flavour package data. A `vars.<flavour>` file defines each flavour's architectures, description, and bootloader. If a flavour has a `<flavour>.inclusion-list` (in Noble Numbat, only `generic` does), it lists the modules shipped in the main `linux-modules` package and the remaining modules go to `linux-modules-extra`. Flavours without an inclusion list ship all modules in `linux-modules`. From Resolute Raccoon (26.04) there are no inclusion lists and no `linux-modules-extra` package. |
| `debian.<kernel>/rules.d/` | Per-architecture build rules (`amd64.mk`, `arm64.mk`, and similar) included by `debian/rules`. |
| `debian.<kernel>/dkms-versions` | Versions of {term}`DKMS` modules built alongside the kernel, for example zfs, ipu6, iwlwifi, and v4l2loopback. Present up to Questing Quokka (25.10); from Resolute Raccoon (26.04) these modules are built by the separate `linux-main-modules` source package instead. |
| `debian.<kernel>/upstream-stable` | Records which upstream stable patch sets have been incorporated into the tree. |
| `debian.<kernel>/modprobe.d/` | `modprobe` configuration shipped with the kernel packages. |
| `debian.<kernel>/copyright` | Copyright file. The build copies it to `debian/copyright`. From Resolute Raccoon (26.04), the tree stores `debian/copyright` directly instead. |

## Maintained versus generated files

Some familiar Debian packaging files do not exist in a fresh clone of the
tree. `debian/rules` generates them from the files described above:

| Generated file | Generated from |
| -------------- | -------------- |
| `debian/control` | `debian.<kernel>/control.stub.in`, the stubs in `debian/control.d/` and `debian.<kernel>/control.d/`, and the version in `debian.<kernel>/changelog`. |
| `debian/changelog` | `debian.<kernel>/changelog` |
| `debian/copyright` | `debian.<kernel>/copyright` (maintained directly in `debian/` from Resolute Raccoon (26.04)) |
| `debian/canonical-certs.pem`, `debian/canonical-revoked-certs.pem` | The certificates in `debian/certs/` and `debian/revoked-certs/` |

Always edit the maintained source files under `debian/` and
`debian.<kernel>/`, never the generated files. `fakeroot debian/rules clean`
recreates the generated files, and `fakeroot debian/rules distclean` removes
the generated `control`, `changelog`, and `copyright` files.

## Version, ABI, and upload numbers

The top entry of `debian.<kernel>/changelog` has the form:

```{code-block} text
linux (6.8.0-90.91) noble; urgency=medium
```

The version has three parts, `<base>-<ABI>.<upload>`:

- **Base** (`6.8.0`): the upstream version the tree is based on. It stays
  fixed as upstream stable updates are absorbed; the top-level `Makefile`
  records the actual stable level of the tree (for example, 6.8.12).
- **ABI number** (`90`): identifies an {term}`ABI` generation of the kernel.
  It appears in the running kernel version reported by `uname -r` (for
  example, `6.8.0-90-generic`) and in the binary package names.
- **Upload number** (`91`): incremented alongside every ABI bump, but may
  increment on its own, for example when a kernel is re-uploaded to fix a
  packaging problem.

When you build a kernel locally, change the ABI number so your packages do
not conflict with the official ones. The
{doc}`kernel build guide </how-to/develop-customise/build-kernel>` uses `999`
for this.

```{note}
Debian package versions are compared with a defined sort order, and some
characters in the version have special meaning. A tilde (`~`) sorts lower
than everything else, including the end of the version string, so
`6.8.0-90.91~test1` sorts before the official `6.8.0-90.91` and is
replaced by that official upload when it becomes available. Other suffixes,
such as `+test1`, sort higher than the plain version, so
`6.8.0-90.91+test1` stays installed over the official `6.8.0-90.91`.
Check an ordering with `dpkg --compare-versions`.
```

## Binary packages built from the tree

A build of the tree produces several binary packages, where `<ver>` is the
base and ABI number (for example, `6.8.0-147`) and `<flavour>` is the flavour
name, such as `generic` or `generic-64k`. The main ones are:

| Package | Contents |
| ------- | -------- |
| `linux-image-unsigned-<ver>-<flavour>` | The kernel image (`vmlinuz`), without a Secure Boot signature. The `linux-signed` source package repackages it with a signature. In trees that build no signed images, the package is named `linux-image-<ver>-<flavour>` instead. |
| `linux-modules-<ver>-<flavour>` | The kernel modules (only those in the flavour's inclusion list, if it has one), plus the `/boot/config-*` and `/boot/System.map-*` files. From Resolute Raccoon (26.04), this package contains all the modules. |
| `linux-modules-extra-<ver>-<flavour>` | The modules not in the inclusion list. Only built for flavours that have one, and not built from Resolute Raccoon (26.04). |
| `linux-headers-<ver>`, `linux-headers-<ver>-<flavour>` | The headers needed to build out-of-tree modules against this kernel, split into a common part and a flavour-specific part. |
| `linux-tools-<ver>-<flavour>` | User space tools built against this kernel, such as `perf`. |

The tree also builds packages for debugging, cloud tools, documentation, and
user space API headers (`linux-libc-dev`), some of them only from the main
`linux` package.

```{note}
The set of binary packages changes between releases. Check the
generated `debian/control` of the tree you are building for the exact list.
```

To install a locally built kernel, follow
{doc}`/how-to/develop-customise/build-kernel`.

## Companion source packages

The main kernel tree is accompanied by separate source packages that track
its version:

- `linux-meta` provides the {term}`linux-meta` meta-packages, such as
  `linux-generic`, which always depend on the latest kernel packages.
- `linux-signed` provides the {term}`linux-signed` packages, which contain
  the kernel images signed for Secure Boot.
- `linux-restricted-modules` provides proprietary modules that cannot ship in
  the main kernel packages, such as the NVIDIA graphics drivers, built
  against a specific kernel ABI.
- `linux-main-modules` (Resolute Raccoon 26.04 and newer) builds the modules
  that older releases build through `debian.<kernel>/dkms-versions`, such as
  zfs, v4l2loopback, ipu6, iwlwifi, and usbio.

## Related topics

- {doc}`/how-to/source-code/obtain-kernel-source-git`
- {doc}`/how-to/develop-customise/build-kernel`
- {doc}`/reference/ubuntu-kernel-configuration`
- {doc}`/reference/glossary`
