---
myst:
  html_meta:
    description: "Test an unmodified upstream kernel to investigate whether an issue comes from Ubuntu's patches or has been fixed upstream."
---

```{owners} team:ckt-tnt
```

(how-to-test-mainline-kernel)=

# How to test a bug with a mainline kernel

```{warning}
Mainline build kernels are unsupported, unsuitable for production, and never
receive security updates. Remove them once you've finished testing.
```

When you encounter an Ubuntu kernel bug, testing an unmodified upstream kernel
can help you determine whether an issue is specific to Ubuntu's kernel patches
or has already been fixed upstream.

The Ubuntu Kernel Team publishes mainline builds using upstream kernel source
and Ubuntu kernel configuration files; these are packaged as `.deb` files which
are ready to be installed.

This guide shows you how to select, verify, install, and remove one of these
mainline builds.

```{seealso}
- For background, see {doc}`/explanation/about-mainline-builds`.
- For file names and archive layout, see {doc}`/reference/mainline-builds`.
- To test kernels that Ubuntu has built but not yet released, see
  {doc}`/how-to/testing-verification/test-pre-release-kernels`.
```

(how-to-mainline-before-you-start)=

## Before you start

- **Use an installed system.** You are recommended to install the mainline
  kernel in an installed environment, restart, and choose the new kernel at
  boot.
- **Remove out-of-tree modules.** If you use proprietary or out-of-tree modules,
  such as the NVIDIA proprietary driver or VirtualBox, uninstall them first.
- **Note your current kernel.** Run {manpage}`uname(1)` with the `-r` option,
  so you can tell your normal kernel from the test kernel later.
- **Check your architecture.** Run `dpkg --print-architecture`.

## Choose a version

Choose a tagged build from the [mainline archive]. Start with the latest stable
version when checking whether upstream has fixed an issue. To locate when a
regression began, test tagged versions on either side of the known working and
broken versions.

Optionally, use the [Ubuntu to mainline version mapping] to find the upstream
release that your current Ubuntu kernel is based on. This helps you choose
versions on either side of it.

## Download the files

Open the directory for the version you chose and check the build status for
your architecture. If the build failed, choose another version.

Open the directory for your architecture and download all `.deb` files for
**one** available flavor. Available flavors vary by architecture and kernel
version. Don't mix files from different flavors or builds.

For example, a complete `generic` package set for `amd64` normally contains:

- common headers, with a file name ending in `_all.deb`
- architecture- and flavor-specific headers
- the kernel image
- kernel modules

Download `CHECKSUMS` and `CHECKSUMS.gpg` from the same architecture directory.
Keep the packages and checksum files in a dedicated directory.

```{seealso}
For details about the package names, see {ref}`ref-mainline-package-files`.
```

## Verify the downloaded files

```{warning}
A compromised kernel can compromise the entire system. Verify every kernel
package before you install it.
```

1. Import the mainline builder's signing key from the Ubuntu keyserver:

   ```{code-block} bash
   gpg --keyserver hkps://keyserver.ubuntu.com --recv-key "60AA7B6F30434AE68E569963E50C6A0917C622B0"
   ```

1. Display the imported key's fingerprint:

   ```{code-block} bash
   gpg --fingerprint "60AA7B6F30434AE68E569963E50C6A0917C622B0"
   ```

   The output should match the value below:

   ```{code-block} text
   pub   rsa2048 2008-05-01 [SC]
         60AA 7B6F 3043 4AE6 8E56  9963 E50C 6A09 17C6 22B0
   uid           [ unknown] Kernel PPA <kernel-ppa@canonical.com>
   ```

1. Check that `CHECKSUMS` was signed with that key, using {manpage}`gpg(1)`:

   ```{code-block} bash
   gpg --verify CHECKSUMS.gpg CHECKSUMS
   ```

   You should see `Good signature from "Kernel PPA <kernel-ppa@canonical.com>"`.
   A warning that the key isn't certified with a trusted signature is expected,
   because you haven't marked the key as trusted. Compare the key's fingerprint
   with the one in the reference instead.

   ```{code-block} bash
   gpg: Signature made Wed 19 Aug 2026 08:18:38 PM +08
   gpg:                using RSA key 60AA7B6F30434AE68E569963E50C6A0917C622B0
   gpg: Good signature from "Kernel PPA <kernel-ppa@canonical.com>" [unknown]
   gpg: WARNING: This key is not certified with a trusted signature!
   gpg:          There is no indication that the signature belongs to the owner.
   Primary key fingerprint: 60AA 7B6F 3043 4AE6 8E56  9963 E50C 6A09 17C6 22B0
   ```

1. Check the downloaded files against the checksums:

   ```{code-block} bash
   shasum -c CHECKSUMS 2>&1 | grep 'OK$'
   ```

   You should get a line ending in `OK` for each downloaded `.deb` file and for
   each type of checksum listed in `CHECKSUMS`. If a file is missing from the
   output, don't install it.

## Install the kernel

Change to the dedicated directory that contains the downloaded files, then
install all the packages with {manpage}`dpkg(1)`:

```{code-block} bash
sudo dpkg -i ./*.deb
```

### Resolve installation failures

If `dpkg` reports an error, match it against the following causes.

- A module fails to build

  A Dynamic Kernel Module Support (DKMS) error mentions VirtualBox or another
  out-of-tree module. Uninstall the module, as described in
  {ref}`how-to-mainline-before-you-start`, then repeat the kernel installation.

- Unsatisfied dependencies

  The error is similar to `depends on <package> (>= <version>); however:
  Package <package> is not installed`.

  - If the package is installed but the version is older than required, you
    need a newer Ubuntu release before you can use this kernel.
  - If the package isn't installed, and the version in your release is new
    enough, install it, then repeat the installation.

- Any other failure

  Check the build status and log in the archive. If the build failed or its
  packages are incomplete, try the next most recent suitable version.

## Boot and test

1. Reboot your system. To reach the boot menu on a BIOS system, hold
   {kbd}`Shift` during startup. On a UEFI system the key varies, often
   {kbd}`Esc`.
1. Select **Advanced options for Ubuntu**.
1. Select the new entry, which looks like `Ubuntu with Linux <version>-generic`.
1. Confirm the running kernel with `uname -r` and record its version, then try
   to reproduce your issue.
1. If a Launchpad bug report exists for your issue, report your test results
   and findings in that bug.

## Return to your normal kernel

Once you've completed the necessary testing, make sure to remove the mainline
build and return to your original kernel.

1. Reboot and select your normal Ubuntu kernel from the same menu.

   Mainline kernels use a separate application binary interface (ABI) namespace,
   so they install alongside Ubuntu kernels. Remove the mainline kernel anyway,
   because it never receives security updates.

1. List the installed kernel packages:

   ```{code-block} bash
   dpkg -l | grep "linux\-[a-z]*\-"
   ```

1. Purge the packages that belong to the mainline kernel with {manpage}`apt(8)`:

   ```{code-block} bash
   sudo apt purge <KERNEL_PACKAGES_TO_REMOVE>
   ```

   Match the version in each package name to the mainline kernel version you
   recorded while testing. **Do not** remove the packages for your normal Ubuntu
   kernel. One kernel version typically includes common headers,
   architecture-specific headers, an image, and modules.

## Related topics

- {doc}`/explanation/about-mainline-builds`
- {doc}`/reference/mainline-builds`
- {doc}`/how-to/testing-verification/test-pre-release-kernels`

% LINKS

[mainline archive]: https://kernel.ubuntu.com/mainline/?C=N;O=D
[Ubuntu to mainline version mapping]: https://people.canonical.com/~kernel/info/kernel-version-map.html