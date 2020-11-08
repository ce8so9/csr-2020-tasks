ezexfil
=======

## Status
* Tech: Done
* Meta: Done

## Description

Service is running qemu emulator with Debian.

User is dropped to a low privilege serial shell, meanwhile root is logged into tty1.

usbip support is compiled into the kernel, usbip tool is available with suid permissions

Exploit by attaching a USB keyboard to the VM and typing blindly into the open root shell.

** !`docker/disk.qcow2` is hosted using git-lfs! **

There should be no mention about USB anywhere on the task.

## CTF Description

Data exfiltration is easy.

## Infos

* Author: lukas2511
* Ports: 7553
* Category: misc
* For Downloading: -
* Flag: CSR{UNR35TR1CT3D_USB_1S_B4D_F0R_Y0UR_0PS3C}
* Points: 250

