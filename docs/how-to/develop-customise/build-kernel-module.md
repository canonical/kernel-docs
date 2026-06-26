---
myst:
  html_meta:
    description: "How to rebuild a single Ubuntu kernel module out-of-tree to quickly test a patch, without rebuilding the entire kernel."
---

# How to rebuild a single kernel module

If you have a patch for a specific kernel driver and want to test it quickly,
you can rebuild just that module out-of-tree instead of rebuilding the entire
kernel. This approach is significantly faster and is well suited for iterating
on a driver fix.

```{important}
Modules built using this method are not intended for use in production.
For managing kernel modules across kernel upgrades, consider using
{manpage}`dkms(8)` instead.
```

## Prerequisites

- The kernel version for which you are rebuilding the module must match the
  running kernel (`uname -r`).
- The driver patch you intent to apply.

### Install required packages

```{code-block} shell
sudo apt update && sudo apt install -y linux-source build-essential
```

## Obtain and patch the kernel source

Install the kernel source package and extract it to your working directory:

```{code-block} shell
sudo apt install -y linux-source
tar xjf /usr/src/linux-source-$(uname -r | cut -d- -f1).tar.bz2
```

```{note}
The tarball name uses the base kernel version (e.g. `linux-source-6.8.0.tar.bz2`),
not the full ABI version string reported by `uname -r`.
```

Apply your patch to the extracted source tree:

```{code-block} shell
cd linux-source-$(uname -r | cut -d- -f1)
patch -p1 < /path/to/your.patch
```

## Set up the out-of-tree build directory

Create a separate build directory and populate it with the build artefacts from
the running kernel:

```{code-block} shell
cd ~
mkdir build_module

cp /lib/modules/$(uname -r)/build/.config    ./build_module/
cp /lib/modules/$(uname -r)/build/Module.symvers ./build_module/
cp /lib/modules/$(uname -r)/build/Makefile   ./build_module/
```

## Prepare the build environment

From inside the kernel source tree, prepare the out-of-tree build directory:

```{code-block} shell
cd linux-source-$(uname -r | cut -d- -f1)

make O=../build_module outputmakefile
make O=../build_module archprepare
```

```{note}
If `archprepare` fails with an error, run `make mrproper` in the source
directory, re-copy the three files from `/lib/modules/$(uname -r)/build/`
as shown in the previous step, then retry rerunning from
`make O=../build_module outputmakefile`.
```

Complete the build preparation:

```{code-block} shell
make O=../build_module prepare
make O=../build_module M=scripts
```

## Build the module

Build only the driver subdirectory containing your change. Replace
`drivers/<path/to/driver>` with the actual path relative to the kernel source
root (for example, `drivers/net/ethernet/intel/e1000e`):

```{code-block} shell
make O=../build_module M=drivers/<path/to/driver> modules
```

The compiled module file (`<driver>.ko`) will appear inside
`build_module/drivers/<path/to/driver>/`.

## Install the module

Copy the new `.ko` file over the existing one in the live module tree:

```{code-block} shell
sudo cp build_module/drivers/<path/to/driver>/<driver>.ko \
    /lib/modules/$(uname -r)/kernel/drivers/<path/to/driver>/
```

## Load and test the module

Unload the old module if it is currently loaded, then load the new one:

```{code-block} shell
sudo modprobe -r <driver>
sudo modprobe <driver>
```

Confirm the module loaded successfully:

```{code-block} shell
lsmod | grep <driver>
dmesg | tail -20
```

Test and verify that your patch is working as intended.
