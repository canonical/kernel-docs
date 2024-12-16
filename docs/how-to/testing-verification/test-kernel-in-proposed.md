# How to test kernels in -proposed

Ubuntu kernels are uploaded to the -proposed pocket for testing before being
published to -updates and -security. You can download these pre-release kernels
to install and test them before a stable release, but you must opt in to package
from -proposed as they are not enabled by default.

## Enable the -proposed pocket to software sources

To install packages from -proposed, you need to enable the relevant source
repositories.

### Enable the -proposed pocket via GUI

1. Open "Software & Updates".
1. Go to the "Developer Options" tab.
1. Enable the {guilabel}`Pre-released updates (<series>-proposed)` option.

### Enable the -proposed pocket via CLI

`````{tab-set}
````{tab-item} Noble Numbat 24.04 (and newer)

Add "\<series\>-proposed" (e.g. "noble-proposed") to the `Suites:` line in the 
{file}`/etc/apt/sources.list.d/ubuntu.sources` file.
```{code-block} text
:emphasize-lines: 3

Types: deb
URIs: http://archive.ubuntu.com/ubuntu
Suites: noble noble-updates noble-backports <series>-proposed
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```
````
````{tab-item} Mantic Minotaur 23.10 (and older)

Add "\<series\>-proposed" (e.g. "jammy-proposed") to the following line in:

- {file}`/etc/apt/sources.list`:
  ```{code-block} text
  deb http://archive.ubuntu.com/ubuntu/ <series>-proposed restricted main multiverse universe
  ```

- {file}`/etc/apt/sources.list` (for non-x86 architectures):
  ```{code-block} text
  deb http://ports.ubuntu.com/ubuntu-ports <series>-proposed restricted main multiverse universe
  ```
````
`````

## Install the pre-release kernel

First, update the sources cache:

```{code-block} none
sudo apt update
```

Then proceed to install the kernel using either a metapackage or a specific
ABI-named image.

### Install via kernel metapackage

Use this approach if you want to receive automatic updates for the latest
version of the kernel in that series.

If the kernel version in -proposed is the highest in any pocket, run:

```{code-block} none
sudo apt install linux-<flavor>
```

If you want a specific (earlier) version of a metapackage, include the version
in the command:

```{code-block} none
sudo apt install linux-<flavor>=<version>
```

### Install via ABI-named kernel image

Use this method to install a specific kernel version without being tied to the
kernel series metapackage.

```{code-block} none
sudo apt install linux-image-<abi>-<flavor>
```

### Boot into the new kernel

After installing the kernel, reboot your machine. After booting up again, verify
that the correct kernel is loaded with:

```{code-block} none
uname -r
```

This should print the correct kernel version and flavor.

## Test the kernel

Once you have the new kernel installed, testing can begin.

If you do not have your own test suite and need an example workload, you can
start with the [built-in Linux selftests]. To run these selftests, download the
kernel source and compile the tests.

```{code-block} none
apt source linux-image-unsigned-$(uname -r)
cd <kernel_source_working_directory>
sudo make -C tools/testing/selftests run_tests
```

For other examples of kernel testing projects, see:

- [Linux Test Project]
- {spellexception}`[stress-ng]`


### Report regression bugs

If you encounter a regression or bug while testing the kernel, please file a bug
report on Launchpad. You can submit your report using any of the following
methods:

1. Run the `ubuntu-bug` tool on the system with the newly installed kernel.

   ```{code-block} none
   ubuntu-bug
   ```

1. Manually file a bug online at <https://bugs.launchpad.net/ubuntu/+filebug>.
Make sure to target the correct kernel source package and Ubuntu series.

For more information on Ubuntu bug reporting, see [Reporting Bugs].

## Related topics

- [Ubuntu Wiki - Enable Proposed]

[built-in Linux selftests]: https://docs.kernel.org/dev-tools/kselftest.html
[Linux Test Project]: https://linux-test-project.readthedocs.io/en/latest/
[stress-ng]: https://github.com/ColinIanKing/stress-ng
[Reporting Bugs]: https://help.ubuntu.com/community/ReportingBugs
[Ubuntu Wiki - Enable Proposed]: https://wiki.ubuntu.com/Testing/EnableProposed
