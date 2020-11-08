

# This file was *autogenerated* from the file expl/expl.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_110776810574249109761224869409352747034539316808708438422202733994614718613548 = Integer(110776810574249109761224869409352747034539316808708438422202733994614718613548); _sage_const_115792089237316195423570985008687907853269984665640564039457584007908834671663 = Integer(115792089237316195423570985008687907853269984665640564039457584007908834671663); _sage_const_10701948434107904703534677081135709656158391970022940433382410029282112083773 = Integer(10701948434107904703534677081135709656158391970022940433382410029282112083773)
import sys
# See:
# [1] Washington, Lawrence C. Elliptic curves: number theory and cryptography. Chapman and Hall/CRC, 2003. p. 60

F = GF(_sage_const_115792089237316195423570985008687907853269984665640564039457584007908834671663 )
# Formulate the DLP
P = (F(_sage_const_110776810574249109761224869409352747034539316808708438422202733994614718613548 ), F(_sage_const_10701948434107904703534677081135709656158391970022940433382410029282112083773 ))
Q = (F(int(sys.argv[_sage_const_1 ])),int(sys.argv[_sage_const_2 ]))

u = (P[_sage_const_0 ])/(P[_sage_const_1 ]) 
v = (Q[_sage_const_0 ])/(Q[_sage_const_1 ])

print "secret: ", v/u

