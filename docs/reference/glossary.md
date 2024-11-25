# Kernel glossary

This page is a running list of terminology that is frequently used when talking
about kernels.

```{glossary}
:sorted:

DKMS
  Dynamic Kernel Module Support, or DKMS is a framework that provides support
  for installing supplementary versions of kernel modules in a simplified manner.
  See the dkms manpages for more information.

ABI
  Application Binary Interface, or ABI defines a stable interface between user space
  applications and the kernel. It ensures that the binaries of applications compiled
  for one version of the kernel remain compatible with subsequent versions, as long as the
  ABI remains unchanged.

linux-meta
  Refers to a set of meta-packages in Linux distributions like Ubuntu. These meta-packages do not  
  contain the kernel binaries or source code themselves but instead define dependencies that point  
  to the latest kernel packages. By installing a linux-meta package (e.g. linux-generic), users can  
  ensure they always receive the latest version of a specific kernel series through updates. In  
  the kernel development and {term}`SRU` lifecycle, linux-meta acts as a bridge between the release  
  of new kernel versions and the package manager. When a new kernel version is releasedand marked  
  stable, the linux-meta package is updated to reference the new version, allowing automatic upgrades.  

linux-signed 
  Refers to kernel packages that are cryptographically signed to ensure their integrity and  
  authenticity. These signatures are crucial for secure boot environments, as they enable the  
  system firmware to verify that the kernel has not been tampered with and is from a trusted  
  source. In the kernel {term}`SRU` lifecycle, linux-signed is created after the corresponding  
  unsigned kernel (e.g. linux-image-unsigned-6.8.0-50-generic) has been built. The signing  
  process is part of the release pipeline, ensuring compliance with secure boot requirements  
  and enhancing security in the kernel deployment process. This package works in tandem with  
  the linux-meta package to deliver signed kernel updates.

SRU
  Stands for Stable Release Update, a process in distributions like Ubuntu used to provide important 
  updates to packages, including kernel packages, after the release of a stable version. SRUs deliver 
  fixes for critical bugs, security vulnerabilities, and hardware enablement while ensuring the stability 
  of the system.
```
