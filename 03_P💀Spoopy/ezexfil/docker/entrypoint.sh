#!/bin/ash

cd /
dd if=/dev/zero of=/dev/shm/flag.img bs=16M count=1 status=none
mkfs.vfat -F16 /dev/shm/flag.img
mcopy -i /dev/shm/flag.img /flag.txt ::flag.txt

socat tcp-l:7553,reuseaddr,fork EXEC:"/qemu.sh"
