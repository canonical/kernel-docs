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

Confirm the module loaded successfully:

```{code-block} shell
lsmod | grep <driver>
dmesg | tail -20
```

Test and verify that your patch is working as intended.

To restore the module shipped with the kernel, 
run `sudo modprobe -r <driver>` followed by `sudo modprobe <driver>`.

```{note}
Loading a module with `insmod` affects only the running system and will not 
persist through reboots. 
```
