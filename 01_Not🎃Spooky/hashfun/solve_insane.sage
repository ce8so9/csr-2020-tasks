"""
Creates a system of 168 equations with 200 variables over GF(2),
leading to a Kernel of 32 dimensions.
The first known bytes are used to determine the correct solution.
Or use the python 2 liner in solve_sane.py, lol.
"""
def int_to_binlist(x):
    return list(map(int, list(bin(x)[2:].rjust(8, "0"))))

def intlist_to_binlist(xs):
    m = []
    for x in xs:
        m.extend(int_to_binlist(x))
    return m


sol = vector(intlist_to_binlist([10,30,31,62,27,9,4,0,1,1,4,4,7,13,8,12,21,28,12,6,60]))
print(sol)
FLAG_LEN = 25 * 8
m = []
for i in range(FLAG_LEN - 32):
    mx = FLAG_LEN * [0]
    mx[i] = 1
    mx[i + 4*8] = 1
    m.append(mx)

M = matrix(GF(2), m)
b = M.solve_right(sol)
K = M.right_kernel()


# We know what we have to add to the given solution
# in order to obtain a bitstring starting with "CSR{"
bl = vector(GF(2), intlist_to_binlist(list(map(ord, "CSR{"))) + 168 * [0])
coeffs = bl + b

# We take the solution sage gave us
# and add multiples of the elements of the kernel.
# Since we know the first 32 bits, we know what multiple 
# we want :)
for i in range(32):
    # coeffs[0] = ord(C) - b[0],
    # this way we end up at a solution
    # that starts with a C...
    b += coeffs[i] * K.gens()[i]

flag = "".join(map(chr, [int(str(b[i:i+8]).replace(",","").replace(" ","").replace("(","").replace(")",""), 2) for i in range(0, 200, 8)]))

print(flag)