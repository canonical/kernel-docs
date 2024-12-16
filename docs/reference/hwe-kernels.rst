HWE kernels
===========

This document provides some reference information about Hardware Enablement
(HWE) kernels: the support life cycle, current kernel in development, the next
planned Ubuntu base kernel version, kernel source code, and how to install the
HWE kernels for use on your machine.

Support life cycle for HWE kernels
----------------------------------

HWE kernels are only enabled on Ubuntu long-term support (LTS) releases, and
have similar life cycles as their newer Ubuntu kernel counterparts. They will
typically get rolled off to the next HWE kernel once a new Ubuntu series is
released (until the next LTS).

.. figure:: /_images/ref-hwe-kernel-release-cycle-jammy.svg
   :alt: Typical HWE kernel release cycle

   Example of HWE kernel release cycle for Jammy Jellyfish

The table below summarizes the support life cycle, development and release
schedule, end-of-life (EOL) and Extended Security Maintenance (ESM) dates for
supported and upcoming HWE kernels.

.. _table-ref-HWE-kernel-life cycle-package:

.. table:: HWE kernel life cycle and package details
   :align: center

   +-----------------+------------------------+----------------+----------------------------------------------------------+
   | Ubuntu series   | Ubuntu version         | Kernel version | Key dates                                                |
   +=================+========================+================+==========================================+===============+
   | Noble Numbat    | 24.04.0 LTS            | 6.8            | Release                                  | April 2024    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2029    |
   +-----------------+------------------------+----------------+------------------------------------------+---------------+
   | Jammy Jellyfish | *22.04.5 LTS (HWE)*    | *6.8*          | :ref:`Edge <ref-about-hwe-install-edge>` | *June 2024*   |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | *Release*                                | *August 2024* |  
   |                 |                        |                +------------------------------------------+---------------+  
   |                 |                        |                | *EOL*                                    | *April 2027*  |
   |                 +------------------------+----------------+------------------------------------------+---------------+
   |                 | 22.04.4 LTS (HWE)      | 6.5            | Release                                  | February 2024 |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | August 2024   |
   |                 +------------------------+----------------+------------------------------------------+---------------+
   |                 | 22.04.0 LTS            | 5.15           | Release                                  | April 2022    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2027    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | ESM                                      | March 2032    |
   +-----------------+------------------------+----------------+------------------------------------------+---------------+
   | Focal Fossa     | 20.04.5 LTS (HWE)      | 5.15           | Release                                  | August 2022   |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2025    |  
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | ESM                                      | April 2030    |
   |                 +------------------------+----------------+------------------------------------------+---------------+
   |                 | 20.04.0 LTS            | 5.4            | Release                                  | April 2020    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2025    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | ESM                                      | April 2030    |
   +-----------------+------------------------+----------------+------------------------------------------+---------------+
   | Bionic Beaver   | 18.04.5 LTS (HWE)      | 5.4            | Release                                  | August 2020   |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2023    |  
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | ESM                                      | April 2028    |
   |                 +------------------------+----------------+------------------------------------------+---------------+
   |                 | 18.04.0 LTS            | 4.15           | Release                                  | April 2018    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2023    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | ESM                                      | April 2028    |
   +-----------------+------------------------+----------------+------------------------------------------+---------------+
   | Xenial Xerus    | 16.04.5 LTS (HWE)      | 4.15           | Release                                  | August 2018   |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2021    |  
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | ESM                                      | April 2026    |
   |                 +------------------------+----------------+------------------------------------------+---------------+
   |                 | 16.04.0 LTS            | 4.4            | Release                                  | April 2016    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2021    |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | ESM                                      | April 2026    |
   +-----------------+------------------------+----------------+------------------------------------------+---------------+
   | Trusty Tahr     | 14.04.5 LTS (HWE)      | 4.15           | Release                                  | August 2016   |
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | EOL                                      | April 2019    |  
   |                 |                        |                +------------------------------------------+---------------+
   |                 |                        |                | ESM                                      | April 2024    |
   +-----------------+------------------------+----------------+------------------------------------------+---------------+

.. note::

   HWE kernels that have reached EOL and are no longer under the ESM support
   phase are excluded from the table above.
   See the `Ubuntu kernel release cycle`_ for information.

Installing a HWE kernel
-----------------------

.. tabs::

   .. group-tab:: 24.04 LTS

      *Ubuntu 24.04 LTS (Noble Numbat)*

      By default, Ubuntu Desktop installations of 24.04 default to tracking the
      HWE stack.
      Server installations will default to the general availability (GA) kernel
      and provide the HWE kernel as an option. 
      
      Desktop:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-24.04

      Server:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-24.04

   .. group-tab:: 22.04 LTS

      *Ubuntu 22.04 LTS (Jammy Jellyfish)*

      By default, Ubuntu Desktop installations of 22.04 default to tracking the
      HWE stack.
      Server installations will default to the GA kernel and provide the HWE
      kernel as an option. 
      
      Desktop:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-22.04

      Server:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-22.04

   .. group-tab:: 20.04 LTS

      *Ubuntu 20.04 LTS (Focal Fossa)*

      By default, Ubuntu Desktop installations of 20.04 default to tracking the
      HWE stack.
      Server installations will default to the GA kernel and provide the HWE
      kernel as an option. 
      
      Desktop:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-20.04

      Server:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-20.04

   .. group-tab:: 18.04 LTS

      *Ubuntu 18.04 LTS (Bionic Beaver)*

      By default, Ubuntu Desktop installations of 18.04.2 and newer point
      releases will ship with an updated kernel and X stack.
      Server installations will default to the GA kernel and provide the HWE
      kernel as an option. 
      
      Desktop:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-18.04 xserver-xorg-hwe-18.04

      Server:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-18.04

   .. group-tab:: 16.04 LTS

      *Ubuntu 16.04 LTS (Xenial Xerus)*

      By default, Ubuntu Desktop installations of 16.04.2 and newer point
      releases will ship with an updated kernel and X stack.
      Server installations will default to the GA kernel and provide the HWE
      kernel as an option. 
      
      Desktop:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-16.04 xserver-xorg-hwe-16.04

      Server:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-hwe-16.04

   .. group-tab:: 14.04 LTS

      *Ubuntu 14.04 LTS (Trusty Tahr)*

      By default, Ubuntu Desktop installations of 14.04.2 and newer point
      releases will ship with an updated kernel and X stack.
      Server installations will default to the GA kernel and provide the HWE
      kernel as an option. 
      
      Desktop:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-lts-xenial xserver-xorg-core-lts-xenial xserver-xorg-lts-xenial xserver-xorg-video-all-lts-xenial xserver-xorg-input-all-lts-xenial libwayland-egl1-mesa-lts-xenial


      Server:

      .. code:: shell

         sudo apt-get install --install-recommends linux-generic-lts-xenial

.. _ref-about-hwe-install-edge:

Installing an edge HWE kernel
-----------------------------

.. note::

   Edge variants of HWE kernels are considered to be in development mode and are
   not supported. These edge variants may have missing components, missing
   :term:`DKMS`, or contain bugs. Edge HWE kernels are not stable releases and
   should not be used in a production environment.

You can get early access to the next HWE kernel - that will be shipped with a
newer kernel version - by installing the ``-edge`` variant.

To install the latest edge kernel variant for Ubuntu 22.04 LTS, run:

.. code:: shell

   sudo apt-get install --install-recommends linux-generic-hwe-22.04-edge

For more information, see :term:`edge kernel` for more information.

Reporting bugs on HWE kernels
-----------------------------

There are two recommended approaches to report a bug against a HWE kernel
package.

1. Using the ``apport-bug`` command.

   .. code:: bash

      apport-bug linux

#. Through the "Report a bug" form for the ``linux`` package in Launchpad:
   https://bugs.launchpad.net/ubuntu/+source/linux/+filebug.

Related topics
--------------

- See the `Stable Updates Cycles`_ for the dates of the last day for kernel
  patches (for HWE kernels) for each stable update cycle.
- See the `Ubuntu kernel release cycle`_ for more details about the kernel
  support life cycle, including the ESM support phase.
- See the `Ubuntu kernel life cycle and enablement stack`_ for more details about
  HWE kernels and their support status.  

.. LINKS

.. _Stable Updates Cycles: https://kernel.ubuntu.com/
.. _Ubuntu kernel release cycle: https://ubuntu.com/about/release-cycle#ubuntu-kernel-release-cycle
.. _Ubuntu kernel life cycle and enablement stack: https://ubuntu.com/kernel/life cycle