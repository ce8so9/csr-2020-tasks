known = b"CSR{"

sols = [10,30,31,62,27,9,4,0,1,1,4,4,7,13,8,12,21,28,12,6,60]

for i in range(21):
    known += chr(sols[i] ^ known[i]).encode()

print(known.decode())