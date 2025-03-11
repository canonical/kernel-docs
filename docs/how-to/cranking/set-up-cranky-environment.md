# How to set up cranky environment

This guide describes the one-off process to configure your build environment to
crank Ubuntu kernels using `cranky`.

## Install dependencies

First, you will need to install the required packages.

### Debian packages

Use apt to install the following debian packages:

```{code-block} text
sudo apt install \
    bash-completion \
    build-essential \
    ccache \
    debhelper \
    devscripts \
    docbook-utils \
    fakeroot \
    gawk \
    git \
    git-email \
    kernel-wedge \
    libncurses5-dev \
    makedumpfile \
    python3-git \
    python3-launchpadlib \
    python3-requests \
    python3-ruamel.yaml \
    schroot \
    sharutils \
    transfig \
    ubuntu-dev-tools \
    wget \
    xmlto
```

### Snapcraft package

Install snapcraft according to the Ubuntu release running on your build machine.

```{tip}
You can check your release of Ubuntu by running `lsb_release -a`.
```

`````{tab-set}
````{tab-item} 24.04 LTS (Noble Numbat) or later

Install `snapcraft` using snap:

```{code-block} text
snap install snapcraft --classic
```
````

````{tab-item} 22.04 LTS (Jammy Jellyfish) or earlier

Install `snapcraft` using apt:

```{code-block} text
sudo apt install snapcraft
```
````

`````



