JSLOVE
====

## Description

PWNing quickjs. There is a known (apparently the maintainers do not know?) bug in quicks which will lead to a controllable UAF.
Out of this one can craft addrof/fakeobj primitives and get an arbitrary r/w primitive e.g. by modifying the Uint32Array object.
Popping a shell is now as easy as allocating and freeing a huge js object to leak libc base, overwriting the realloc hook with system, extending an array with the first element set to /bin/sh (e.g. encoded as a floating point number).

## CTF Description

Better Be Quick.
https://twitter.com/_niklasb/status/1154392571466125313

## Infos

* Author: kowu
* Ports: 29546
* Category: pwn
* For Downloading: better-be-quick-8f2917eb0fd326a0cbddc0102987c96d.tar.xz
* Flag: CSR{fuggg-it-finally-got-patched...}
* Points: 500
