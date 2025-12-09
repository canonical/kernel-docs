# How to build an Ubuntu Linux kernel snap

If you are running an Ubuntu Core system and want to use boot into a custom
kernel, you will need a kernel snap.

This guide shows how to build a kernel snap for local development and testing.

```{important}
Kernel snaps built using this method are not intended for use in production.
```

## Prerequisites

Before you begin, you will need:

- A Launchpad account
- To be part of the Launchpad team that owns the project (for private
repositories)
- A build machine running Ubuntu
- A device running an Ubuntu Core image with "dangerous" model assertion grade
to install the custom kernel snap

  ```{note}
  The Ubuntu version of the build host must match the version of the device
  where the kernel snap will be installed.
  For example, use an Ubuntu 22.04 (Jammy) host to build the kernel snap for an
  Ubuntu Core 22 device.  
  See [Snap - Build environment options] for more information.
  ```

## Set up build environment

Set up the host machine which will be used to build the kernel snap.

### Install snapcraft

Snapcraft is used to create a managed environment to build the kernel snap. You
are recommended to use the latest/stable version of the snapcraft snap from the
Snap Store.

On the build machine, remove any existing snapcraft debian package and install
snapcraft by running:

```{code-block} shell
sudo apt-get update
sudo apt-get -y upgrade
sudo apt purge -y snapcraft
sudo snap install snapcraft --classic
```

### Configure source repositories

Configure the package source repositories for the host architecture by
specifying the architecture (e.g. "[arch=amd64]" for x86-64 hosts) for each deb
source list in the data sources file.

`````{tab-set}
````{tab-item} Ubuntu 24.04 (Noble) and newer

Update the `/etc/apt/sources.list.d/ubuntu.sources` file. For example, on a
x86-64 host running Ubuntu 24.04 (Noble):

```{code-block} text
:emphasize-lines: 6

[...]
Types: deb deb-src
URIs: http://archive.ubuntu.com/ubuntu
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Architectures: amd64
[...]
```
````

````{tab-item} Ubuntu 23.10 (Mantic) and older

Update the `/etc/apt/sources.list` file. For example, on a x86-64 host running
Ubuntu 22.04 (Jammy):

```{code-block} text
deb [arch=amd64] http://archive.ubuntu.com/ubuntu focal main restricted
```

Alternatively, if you are running a default installation of Ubuntu, you can do a
global update of all sources in the `/etc/apt/sources.list` file.

```{code-block} shell
sudo sed -ie 's/deb http/deb [arch=amd64] http/g' /etc/apt/sources.list
```
````
`````

### Add support for cross-compilation

Add the target architecture (e.g. "arm64") to the list of supported
architectures. This step is only required if the build machine is running on a
different architecture than the target device for the kernel snap.

For example, if you want to build a kernel snap for an ARM64 device on a x86-64 
host, run:

```{code-block} shell
sudo dpkg --add-architecture arm64
sudo apt update
```

Confirm that support for the target architecture has been added successfully by
running <code>dpkg &#45;\&#45;print-foreign-architectures</code>:

```{terminal}
:user: user
:host: host

dpkg --print-foreign-architectures

arm64
```

### Configure SSH settings for Launchpad access

Enable SSH access to `git.launchpad.net` for your Launchpad account. This step is only required if you are building a snap from a private repository in Launchpad.

Add the following in the {file}`~/.ssh/config` file:

```{code-block} text
Host git.launchpad.net
  User <your Launchpad username>
```

## Clone the kernel snap recipe

Once you have set up your host machine, clone the Ubuntu Linux kernel snap recipe.

```{code-block} shell
git clone <kernel-source-repository>
```

## Customize the kernel

Add any firmware or binary blobs, or customize `initrd` as needed. This step is only required if you want to make your own changes to the kernel.

% TODO - create a template snapcraft.yaml file for any project

## Build the kernel snap

You are now ready to build the kernel snap.

1. Go to the directory with the cloned kernel repository.
   ```{code-block} shell
   cd <kernel-source-repository>
   ```
1. Create an alias for the {file}`snapcraft.yaml` file. This is only required if there are multiple YAML configuration files in the {file}`snap/local/` tree.
   ```{code-block} shell
   ln -s snap/local/<project>.yaml snapcraft.yaml
   ```
1. (Optional) Add the `sed` command in the {file}`snapcraft.yaml` file to set the Kconfig value `CONFIG_MODULE_SIG_ALL` to `n` for your target architecture. This allows unverified modules to be loaded into the kernel and should only be set to `n` for local testing and development.

   For example, if the kernel snap is for an ARM64 device, set `'arm64': 'n'`:
   ```{code-block} yaml
   :emphasize-lines: 8
   [...]
   parts:
     kernel:
       override-build: |
         [...]
         # override configs
         sed -i "s/^\(CONFIG_MODULE_SIG_FORCE\).*/\\1 policy\<{'arm64': 'n', 'armhf': 'n'}\>/" ${DEBIAN}/config/annotations
         sed -i "s/^\(CONFIG_MODULE_SIG_ALL.*\)'arm64': 'y'\(.*\)/\\1'arm64': 'n'\\2/" ${DEBIAN}/config/annotations
         [...]
   ```
1. Build the kernel snap package.
   `````{tab-set}
   ````{tab-item} UC24 and UC22
   ```{code-block} shell
   sudo snapcraft --build-for=arm64 --destructive-mode
   ```
   ````
   ````{tab-item} UC20
   ```{code-block} shell
   sudo snapcraft --target-arch=arm64 --destructive-mode --enable-experimental-target-arch
   ```
   ````
   `````
1. You should get a {file}`<name>_<version>_<arch>.snap` file in the kernel repository root, where:
   - `<name>` is the identified set in {file}`snapcraft.yaml`
   - `<version>` is the kernel version 
   - `<arch>` is the target architecture for the kernel snap
1. Copy the kernel snap to your target device and reboot into latest kernel to verify your changes.
   ```{code-block}
   snap install --dangerous --devmode <name>_<version>_<arch>.snap
   ```

   ```{note}
   Local snaps can only be installed if the Ubuntu Core image on the target device was created with a model assertion that  specifies the "dangerous" grade.
   ```


% LINKS
[Ubuntu Wiki - Build your own kernel]: https://wiki.ubuntu.com/Kernel/BuildYourOwnKernel
[Snap - Build environment options]:  https://documentation.ubuntu.com/snapcraft/stable/reference/build-environment-options/
