#!/bin/sh

timeout 120 qemu-system-x86_64 \
	-M pc-i440fx-3.1 \
	-netdev user,id=net0,net=10.0.2.0/24 \
	-device virtio-net,netdev=net0 \
	-drive file=disk.qcow2,format=qcow2,if=virtio,readonly \
	-drive file=/dev/shm/flag.img,format=raw,if=virtio,readonly \
	-m 48M \
	-serial stdio \
	-monitor none \
	-display none

echo "Session timed out :("
