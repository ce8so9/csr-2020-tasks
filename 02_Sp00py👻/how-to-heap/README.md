how to heap
====

## Description

Archlinux has some new mitigations for the glibc tcache, which should prevent some attack scenarios.
They should be introduced to other distros sooner or later. Basic heap exploitation with oob read/write primitive functionality.

leak libc & heap base, modify tcache next ptr (circumvent the new xor protection), spawn chunk at free hook, overwrite free hook, call system("/bin/sh").

## CTF Description

Do you even know how to heap? With all those new mitigations around?

## Infos

* Author: kowu
* Ports: 8263
* Category: pwn
* For Downloading: how-to-heap-0594dbc0ced3b3258b20e83fd11a913a.tar.xz
* Flag: CSR{yeeetcc2407abf43d6fa39c0cba68ee25522b}
* Points: 200
