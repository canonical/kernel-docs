---
myst:
  html_meta:
    description: "Reference for the Ubuntu mainline kernel archive and its files."
---

```{owners} team:ckt-tnt
```

(ref-mainline-builds)=

# Mainline kernel archive

```{include} /reuse/mainline-builds-warning.txt
```

The [Ubuntu mainline kernel archive] contains mainline builds published on a
best effort basis by the Kernel Team at Canonical.

To install and test a build, see
{doc}`/how-to/testing-verification/test-with-mainline-kernel`.

## Directory layout

```{list-table}
:header-rows: 1

* - Location
  - Contents
* - `v<version>/`
  - A build for a tagged Linux release or release candidate
* - `v<version>/<architecture>/`
  - Packages, checksums, status, and logs for one architecture
```

A version directory identifies the source commit and reports the build status for
each architecture. The architectures and kernel flavors available depend on the
build.

### Files in an architecture directory

```{list-table}
:header-rows: 1

* - File
  - Purpose
* - `*.deb`
  - Installable kernel packages
* - `CHECKSUMS`
  - Checksums for the published files
* - `CHECKSUMS.gpg`
  - OpenPGP signature for `CHECKSUMS`
* - `log`
  - Complete build log
* - `status`
  - Numeric build status
* - `summary.yaml`
  - Build result and package summary
* - `REBUILD`
  - Information about a rebuilt package set, when present
* - `self-tests/`
  - Build self-test results, when present
```

(ref-mainline-package-files)=

## Package files

Package names identify the kernel version, flavor, build, and architecture.
A typical `generic` package set for `amd64` contains:

```text
linux-headers-<version>_<version>.<build>_all.deb
linux-headers-<version>-generic_<version>.<build>_amd64.deb
linux-image-unsigned-<version>-generic_<version>.<build>_amd64.deb
linux-modules-<version>-generic_<version>.<build>_amd64.deb
```

```{list-table}
:header-rows: 1

* - Package name
  - Contents
* - `linux-headers-<version>_<version>.<build>_all.deb`
  - Headers shared by all architectures and flavors
* - `linux-headers-<version>-<flavor>_<version>.<build>_<architecture>.deb`
  - Headers for one architecture and flavor
* - `linux-image[-unsigned]-<version>-<flavor>_<version>.<build>_<architecture>.deb`
  - Bootable kernel image
* - `linux-modules-<version>-<flavor>_<version>.<build>_<architecture>.deb`
  - Loadable kernel modules
```

The exact package set varies by architecture and build. Some architectures use
`linux-image` instead of `linux-image-unsigned`, and some provide more than one
flavor.

(ref-mainline-signing-key)=

## Signing key

The mainline builder signs `CHECKSUMS` with the following key:

```text
Fingerprint: 60AA 7B6F 3043 4AE6 8E56 9963 E50C 6A09 17C6 22B0
User ID: Kernel PPA <kernel-ppa@canonical.com>
```

Validate the key against its record on the Ubuntu keyserver before relying on
the signature.

## Ubuntu to mainline version mapping

The [Ubuntu kernel version mappings](https://people.canonical.com/~kernel/info/kernel-version-map.html)
table shows which upstream release an Ubuntu kernel is based on. An Ubuntu
kernel isn't identical to the corresponding mainline kernel because Ubuntu
applies its own patches and configuration.

## Related topics

- {doc}`/how-to/testing-verification/test-with-mainline-kernel`
- {doc}`/explanation/about-mainline-builds`
- {doc}`/reference/ubuntu-kernels`

% LINKS

[Ubuntu mainline kernel archive]: https://kernel.ubuntu.com/mainline/?C=N;O=D