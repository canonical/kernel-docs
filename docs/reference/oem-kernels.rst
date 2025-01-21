OEM kernels
===========

.. include:: /reuse/oem-kernels.txt
   :start-after: overview-oem-kernel-start
   :end-before: overview-oem-kernel-end

This document provides some reference information about OEM kernels: the support
life cycle for rolling releases, current kernel in development, the next planned
generic Ubuntu kernel version, kernel source code, and how to install the OEM
kernels for use on your machine.

Support life cycle for OEM kernels
----------------------------------

OEM kernels have shorter life cycles than their generic Ubuntu kernel
counterparts. They will typically get rolled off to the next HWE kernel once all
the fixes have been forward-ported.

The table below summarizes the support life cycle, development and stable release
schedules, EOL dates, and kernel migration target for supported and upcoming OEM
kernels.

.. _table-ref-oem-kernel-life cycle-package:

.. table:: OEM kernel life cycle and package details

   +---------------------------+------------------------------+-------------------------+---------------------------+
   | Kernel and Ubuntu version | Source code and meta package | Key dates               | Migration target          |
   +===========================+==============================+========+================+===========================+
   | 6.5                       | s: `linux-oem-6.5`_          | Devel  | July 2023      | 22.04.5 HWE kernel (6.8)  |
   |                           |                              +--------+----------------+                           |
   | 22.04 LTS (Jammy)         | m: linux-oem-22.04d          | Stable | August 2023    |                           |
   |                           |                              +--------+----------------+                           |  
   |                           |                              | EOL    | July 2024      |                           |
   +---------------------------+------------------------------+--------+----------------+---------------------------+
   | 6.8                       | s: `linux-oem-6.8`_          | Devel  | March 2024     | 24.04.2 HWE kernel (6.11) |
   |                           |                              +--------+----------------+                           |
   | 24.04 LTS (Noble)         | m: linux-oem-24.04a          | Stable | April 2024     |                           |
   |                           |                              +--------+----------------+                           |  
   |                           |                              | EOL    | February 2025  |                           |
   +---------------------------+------------------------------+--------+----------------+---------------------------+
   | 6.11                      | s: `linux-oem-6.11`_         | Devel  | August 2024    | :spellexception:`TBD`     |
   |                           |                              +--------+----------------+                           |
   | 24.04 LTS (Noble)         | m: linux-oem-24.04b          | Stable | November 2024  |                           |
   |                           |                              +--------+----------------+                           |  
   |                           |                              | EOL    | July 2025      |                           |
   +---------------------------+------------------------------+--------+----------------+---------------------------+

.. note::
   OEM kernels that have reached end-of-life (EOL) are excluded from the table
   above.

Selection guidelines for OEM kernels
------------------------------------

In general, we need at least three OEM kernels for each Ubuntu LTS release to
support our OEM projects.

- First OEM kernel

  Released early in the Ubuntu LTS cycle to meet the needs of OEM projects that
  require the latest Ubuntu LTS release. This OEM kernel is based on the Ubuntu
  LTS kernel, with the same kernel version. Normally, this will be migrated to
  the \*.2 :abbr:`HWE (Hardware Enablement)` kernel.
  
- Second OEM kernel

  The second OEM kernel is typically released in the second half of the same
  year as the Ubuntu LTS release, and it is for supporting the latest Intel and
  AMD hardware platforms. It could be based on either the xx.10 Ubuntu kernel or
  the upstream LTS kernel, and may later migrate to the \*.3 or \*.4 HWE kernel.

- Third OEM kernel

  The final OEM kernel introduced in an LTS cycle to support the latest hardware
  near the end of the release timeline. This will be migrated to the \*.5 HWE
  kernel.

These guidelines serve as a reference only and may be adjusted as necessary
to accommodate hardware schedules. 
Additional OEM kernels may be introduced to support cutting-edge hardware
designs and to meet the time-to-market requirements of OEM partners.

Downloading and installing OEM kernels
--------------------------------------

To view and/or download the source code for OEM kernels, go to the kernel
repository (e.g. “s: linux-oem-6.5”) listed in the “Source code and meta
package” column in the :ref:`table-ref-oem-kernel-life cycle-package` table.

To install an OEM kernel, use the meta-package name (e.g. “m: linux-oem-22.04d”)
for the kernel version listed in the “Source code and meta package” column in
the :ref:`table-ref-oem-kernel-life cycle-package` table.
For example, to install OEM kernel version 6.8, run:

.. code:: bash

   apt install linux-oem-24.04a

.. tip::
   Use the meta-package name when installing the OEM kernel to ensure that you
   continue receiving automated updates even after the OEM kernel is rolled off
   to the target migration kernel.

Reporting bugs on OEM kernels
-----------------------------

There are two recommended approaches to report a bug against an OEM kernel
package.

1. Using the ``apport-bug`` command with the OEM kernel package name. For
   example, to report a bug for the "linux-oem-6.8" kernel, run:

   .. code:: bash

      apport-bug linux-oem-6.8

#. Through the "Report a bug" form in Launchpad. For example, to report a bug
   for the "linux-oem-6.8" kernel, go to
   https://bugs.launchpad.net/ubuntu/+source/linux-oem-6.8/+filebug. 

Related topics
--------------

- See the `Stable Updates Cycles`_ for the dates of the last day for kernel
  patches (for OEM kernels) for each stable update cycle.
- See the Gitea repositories for `jammy-linux-oem`_ and `noble-linux-oem`_ for
  pending pull requests and details on the patches that are merged and released
  for each OEM kernel.

.. LINKS

.. _linux-oem-6.5: https://kernel.ubuntu.com/gitea/kernel/jammy-linux-oem/src/branch/oem-6.5-next
.. _linux-oem-6.8: https://kernel.ubuntu.com/gitea/kernel/noble-linux-oem/src/branch/oem-6.8-next
.. _linux-oem-6.11: https://kernel.ubuntu.com/gitea/kernel/noble-linux-oem/src/branch/oem-6.11-next
.. _Stable Updates Cycles: https://kernel.ubuntu.com/
.. _jammy-linux-oem: https://kernel.ubuntu.com/gitea/kernel/jammy-linux-oem/pulls
.. _noble-linux-oem: https://kernel.ubuntu.com/gitea/kernel/noble-linux-oem/pulls