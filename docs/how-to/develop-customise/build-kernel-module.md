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

Use this method when your patch is confined to the driver's own sources.

If your patch changes shared kernel headers, Kconfig options, or the signature
of an exported symbol, the rebuilt module no longer matches the running kernel.
`CONFIG_MODVERSIONS` refuses to load a module whose exported symbol signatures
changed, but it does not detect structure layout changes inside headers. For
those changes, build and boot a complete kernel instead. See
{doc}`/how-to/develop-customise/build-kernel`.

The module is built against the running kernel version (`uname -r`) and works 
only on that version. Installing a different kernel requires rebuilding the 
module.

This guide supports Trusty Tahr and newer.

### Install required packages

```{code-block} shell
sudo apt update && \
    sudo apt install -y linux-source build-essential linux-headers-$(uname -r)
```

```{note}
If you are developing against a custom kernel you will need to manually
install it's headers using `dpkg`, rather than getting Ubuntu kernel headers 
from `apt`.
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

## Build the module

Build only the driver subdirectory containing your change. Replace
`drivers/<path/to/driver>` with the actual path relative to the kernel source
root (for example, `drivers/net/ethernet/intel/e1000e`):

```{code-block} shell
make -C /lib/modules/$(uname -r)/build \
    M=$PWD/drivers/<path/to/driver> modules
```

The compiled module file (`<driver>.ko`) will appear inside
`drivers/<path/to/driver>/`.

## Load and test the module

Unload the old module if it is currently loaded, then load the new one:

```{code-block} shell
sudo modprobe -r <driver>
sudo insmod drivers/<path/to/driver>/<driver>.ko
```

```{important}
On a system with Secure Boot enabled, loading an unsigned module will fail.
Either test on a system with Secure Boot disabled, such as a virtual
machine, or sign the module with an enrolled Machine Owner Key (MOK).
```

Confirm the module loaded successfully:

```{code-block} shell
lsmod | grep <driver>
sudo dmesg | tail -20
```

Test and verify that your patch is working as intended.

To restore the module shipped with the kernel, 
run `sudo modprobe -r <driver>` followed by `sudo modprobe <driver>`.

```{note}
Loading a module with `insmod` affects only the running system and will not 
persist through reboots. 
```

## Make the module persist across reboots

To test the behaviour of a module at boot, install it into the `updates`
directory. `depmod` searches this directory ahead of the one holding the
module shipped with the kernel, so your build takes precedence without
modifying any file owned by a package:

```{code-block} shell
sudo mkdir -p /lib/modules/$(uname -r)/updates
sudo cp drivers/<path/to/driver>/<driver>.ko /lib/modules/$(uname -r)/updates/
sudo depmod -a
modinfo -F filename <driver>
```

The path reported by `modinfo` must be the one under `updates`.

If the driver is in the initramfs, you need to rebuild that too:

```{code-block} shell
lsinitramfs /boot/initrd.img-$(uname -r) | grep <driver>
sudo update-initramfs -u -k $(uname -r)
```

To remove the override, delete the file from `updates`, then rerun `depmod`, and
`update-initramfs` if you rebuilt the initramfs.

```{note}
The override applies only to the kernel version you installed it under.
Installing a new kernel provides a new module tree, and your build is no longer
used.
```
