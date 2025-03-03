# How to enable kernel source package repositories

If you want to build or modify an Ubuntu kernel package from source, you will first need the kernel source code.
This is provided via `deb-src` - a line in the {file}`sources.list` or {file}`ubuntu.sources` file that points to repositories containing source packages instead of pre-built binaries.
`deb-src` will need to be enabled on your build machine.

## Enable `deb-src` for Noble Numbat 24.04 (and newer)

Add "deb-src" to the `Types:` line in the {file}`/etc/apt/sources.list.d/ubuntu.sources` file.

```{code-block} text
:emphasize-lines: 1

Types: deb deb-src
URIs: http://archive.ubuntu.com/ubuntu
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

## Enable `deb-src` for Mantic Minotaur 23.10 (and older)

Check that you have the following entries in the {file}`/etc/apt/sources.list` file.
If not, add or uncomment these lines for your Ubuntu release.
For example, for Jammy:

```{code-block} text
deb-src http://archive.ubuntu.com/ubuntu jammy main
deb-src http://archive.ubuntu.com/ubuntu jammy-updates main
```
