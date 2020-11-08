unhackable
====

## Description

Metachallenge for ctf organizers. Forgot to disable the qemu console.
By pressing ctrl+a and c afterwards, the qemu console is opened. One can dump the physical memory. The flag file is somewhere in there.
There should be no bug inside the kind of unusual linux image (i hope), it is optimized for size so that a stupid dumping approach would only require a maximum of 32MB of data.

## CTF Description

This is unhackable, plain linux with a busybox shell. See for yourself.

## Infos

* Author: kowu
* Ports: 9124
* Category: misc
* For Downloading: unhackable-6a17c789895dbb2960658606c189e38f.tar.xz
* Flag: CSR{534341091511a53e03b694840ab582aa}
* Points: 100
