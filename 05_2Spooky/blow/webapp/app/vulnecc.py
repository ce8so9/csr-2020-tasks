try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


class AffinePoint:

    def __init__(self, curve, x, y, order=None):
        self.curve = curve
        self.x = x
        self.y = y
        self.order = order

    def __add__(self, other):
        return self.curve.add(self, other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __rmul__(self, scalar):
        return self.curve.mul(self, scalar)

    def __str__(self):
        return "Point({},{}) on {}".format(self.x, self.y, self.curve)

    def copy(self):
        return AffinePoint(self.curve, self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, AffinePoint):
            raise ValueError("Can't compare Point to {}".format(type(other)))
        return self.curve == other.curve and self.x == other.x and self.y == other.y


class EllipticCurve:
    def inv_val(self, val):
        """
        Get the inverse of a given field element using the curves prime field.
        """
        return pow(val, self.mod - 2, self.mod)

    def legendre_symbol(self, a):
        ls = pow(a, (self.mod - 1) // 2, self.mod)
        return -1 if ls == self.mod - 1 else ls

    def sqrt(self, a):
        """
        Take the square root in the field using Tonelli–Shanks algorithm.
        Based on https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
        :return: sqrt(a) if it exists, 0 otherwise
        """
        p = self.mod
        if self.legendre_symbol(a) != 1:
            return 0
        elif a == 0:
            return 0
        elif p == 2:
            return p
        elif p % 4 == 3:
            # lagrange method
            return pow(a, (p + 1) // 4, p)

        # Partition p-1 to s * 2^e for an odd s (i.e.
        # reduce all the powers of 2 from p-1)
        s = p - 1
        e = 0
        while s % 2 == 0:
            s //= 2
            e += 1

        # Find some 'n' with a legendre symbol n|p = -1.
        # Shouldn't take long.
        n = 2
        while self.legendre_symbol(n) != -1:
            n += 1

        # Here be dragons!
        # Read the paper "Square roots from 1; 24, 51,
        # 10 to Dan Shanks" by Ezra Brown for more
        # information
        #

        # x is a guess of the square root that gets better
        # with each iteration.
        # b is the "fudge factor" - by how much we're off
        # with the guess. The invariant x^2 = ab (mod p)
        # is maintained throughout the loop.
        # g is used for successive powers of n to update
        # both a and b
        # r is the exponent - decreases with each update
        #
        x = pow(a, (s + 1) // 2, p)
        b = pow(a, s, p)
        g = pow(n, s, p)
        r = e

        while True:
            t = b
            m = 0
            for m in range(r):
                if t == 1:
                    break
                t = pow(t, 2, p)

            if m == 0:
                return x

            gs = pow(g, 2 ** (r - m - 1), p)
            g = (gs * gs) % p
            x = (x * gs) % p
            b = (b * g) % p
            r = m

    def invert(self, point):
        """
        Invert a point.
        """
        return AffinePoint(self, point.x, (-1 * point.y) % self.mod)

    def mul(self, point, scalar):
        """
        Do scalar multiplication Q = dP using double and add.
        """
        return self.double_and_add(point, scalar)

    def double_and_add(self, point, scalar):
        """
        Do scalar multiplication Q = dP using double and add.
        As here: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        """
        if scalar == 0:
            return self.poif
        elif scalar < 0:
            raise ValueError("Scalar must be >= 0")
        result = None
        tmp = point.copy()

        while scalar:
            if scalar & 1:
                if result is None:
                    result = tmp
                else:
                    result = self.add(result, tmp)
            scalar >>= 1
            tmp = self.add(tmp, tmp)

        return result

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def jacobi_symbol(a, n):
    assert (n > a > 0 and n % 2 == 1)
    t = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == n % 4 == 3:
            t = -t
        a %= n
    if n == 1:
        return t
    else:
        return 0


class WeierstrassCurve(EllipticCurve):

    def __init__(self, a, b, mod):
        self.a = a
        self.b = b
        self.mod = mod
        self.poif = AffinePoint(self, "infinity", "infinity")

    def is_singular(self):
        return (-16 * (4 * self.a ** 3 + 27 * self.b ** 2)) % self.mod == 0

    def _exp(self, base, e):
        return pow(base, e, self.mod)

    def calc_y_sq(self, x):
        return (self._exp(x, 3) + self.a * x + self.b) % self.mod

    def is_on_curve(self, point):
        return point is self.poif or self.calc_y_sq(point.x) == self._exp(point.y, 2)

    def enumerate_points(self):
        """
        Yields points of the curve.
        This only works well on tiny curves.
        """
        for i in range(self.mod):
            sq = self.calc_y_sq(i)
            y = self.sqrt(sq)

            if y:
                yield AffinePoint(self, i, y)
                yield AffinePoint(self, i, self.mod - y)

    def plot(self, dotsize=300, fontsize=32):
        """
        Plot the curve as scatter plot.
        This obviously only works for tiny fields.
        :return: pyplot object
        """
        if plt is None:
            raise ValueError("matplotlib not available.")
        x = []
        y = []
        for P in self.enumerate_points():
            x.append(P.x)
            y.append(P.y)

        plt.rcParams.update({'font.size': fontsize})
        plt.scatter(x, y, s=dotsize, marker="o")
        plt.grid()
        plt.title("{}".format(self))

        return plt

    def add(self, P, Q):
        """
         Sum of the points P and Q.
         Rules: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        if not (self.is_on_curve(P) and self.is_on_curve(Q)):
            raise ValueError(
                "Points not on basic_curves {}: {}, {}: {}".format(P, self.is_on_curve(P), Q, self.is_on_curve(Q)))

        # Cases with POIF
        if P == self.poif:
            result = Q
        elif Q == self.poif:
            result = P
        elif Q == self.invert(P):
            result = self.poif
        else:  # without POIF
            if P == Q:
                slope = (3 * P.x ** 2 + self.a) * self.inv_val(2 * P.y)
            else:
                slope = (Q.y - P.y) * self.inv_val(Q.x - P.x)
            x = (slope ** 2 - P.x - Q.x) % self.mod
            y = (slope * (P.x - x) - P.y) % self.mod
            result = AffinePoint(self, x, y)

        return result

    def __str__(self):
        return "y^2 = x^3 + {}x + {} mod {}".format(self.a, self.b, self.mod)


def jacobi_symbol(a, n):
    assert (n > a > 0 and n % 2 == 1)
    t = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == n % 4 == 3:
            t = -t
        a %= n
    if n == 1:
        return t
    else:
        return 0


class WeierstrassCurve(EllipticCurve):

    def __init__(self, a, b, mod):
        self.a = a
        self.b = b
        self.mod = mod
        self.poif = AffinePoint(self, 0, 0)

    def is_singular(self):
        return (-16 * (4 * self.a ** 3 + 27 * self.b ** 2)) % self.mod == 0

    def _exp(self, base, e):
        return pow(base, e, self.mod)

    def calc_y_sq(self, x):
        return (self._exp(x, 3) + self.a * x + self.b) % self.mod

    def is_on_curve(self, point):
        return point is self.poif or self.calc_y_sq(point.x) == self._exp(point.y, 2)

    def enumerate_points(self):
        """
        Yields points of the curve.
        This only works well on tiny curves.
        """
        for i in range(self.mod):
            sq = self.calc_y_sq(i)
            y = self.sqrt(sq)

            if y:
                yield AffinePoint(self, i, y)
                yield AffinePoint(self, i, self.mod - y)

    def plot(self, dotsize=300, fontsize=32):
        """
        Plot the curve as scatter plot.
        This obviously only works for tiny fields.
        :return: pyplot object
        """
        if plt is None:
            raise ValueError("matplotlib not available.")
        x = []
        y = []
        for P in self.enumerate_points():
            x.append(P.x)
            y.append(P.y)

        plt.rcParams.update({'font.size': fontsize})
        plt.scatter(x, y, s=dotsize, marker="o")
        plt.grid()
        plt.title("{}".format(self))

        return plt

    def add(self, P, Q):
        """
         Sum of the points P and Q.
         Rules: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        # don't check if point is on curve to stay vulnerable

        # Cases with POIF
        if P == self.poif:
            result = Q
        elif Q == self.poif:
            result = P
        elif Q == self.invert(P):
            result = self.poif
        else:  # without POIF
            if P == Q:
                slope = (3 * P.x ** 2 + self.a) * self.inv_val(2 * P.y)
            else:
                slope = (Q.y - P.y) * self.inv_val(Q.x - P.x)
            x = (slope ** 2 - P.x - Q.x) % self.mod
            y = (slope * (P.x - x) - P.y) % self.mod
            result = AffinePoint(self, x, y)

        return result

    def __str__(self):
        return "y^2 = x^3 + {}x + {} mod {}".format(self.a, self.b, self.mod)

p = 2**256 - 2**224 + 2**192 + 2**96 - 1
curveP256_vuln = WeierstrassCurve(-3, 41058363725152142129326129780047268409114441015993725554835256314039467401291, p)

G = AffinePoint(
        curveP256_vuln,
        48439561293906451759052585252797914202762949526041747995844080717082404635286,
        36134250956749795798585127919587881956611106672985015071877198253568414405109,
        115792089210356248762697446949407573529996955224135760342422259061068512044369
)

# If we do a scalar multiplication of the generators
# order with the generator point, we should end up
# at the neutral element, the point at infinity
X = G.order * G
assert(X == curveP256_vuln.poif)

# Since the point at infinity is the neutral element,
# with order+1 we should en up at the generator.
X = (G.order + 1) * G
assert(X == G)