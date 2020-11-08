#!/bin/sh

cd /home
timeout 1m qemu-system-x86_64 -kernel bzImage -no-reboot -m 32M --nographic -smp cores=1,threads=1 -append 'console=ttyS0 oops=panic panic=1'
