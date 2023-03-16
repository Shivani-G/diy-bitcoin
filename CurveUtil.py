from Point import Point, G

INF = Point(None, None, None) # special point at "infinity", kind of like a zero

def extended_euclidean_algorithm(a, b):
    """
    Returns (gcd, x, y) s.t. a * x + b * y == gcd
    This function implements the extended Euclidean
    algorithm and runs in O(log b) in the worst case,
    taken from Wikipedia.
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t

def inv(n, p):
    """ returns modular multiplicate inverse m s.t. (n * m) % p == 1 """
    gcd, x, y = extended_euclidean_algorithm(n, p) # pylint: disable=unused-variable
    return x % p

def elliptic_curve_addition(self, other: Point) -> Point:
    # handle special case of P + 0 = 0 + P = 0
    if self == INF:
        return other
    if other == INF:
        return self
    # handle special case of P + (-P) = 0
    if self.x == other.x and self.y != other.y:
        return INF
    # compute the "slope"
    if self.x == other.x: # (self.y = other.y is guaranteed too per above check)
        m = (3 * self.x**2 + self.curve.a) * inv(2 * self.y, self.curve.p)
    else:
        m = (self.y - other.y) * inv(self.x - other.x, self.curve.p)
    # compute the new point
    rx = (m**2 - self.x - other.x) % self.curve.p
    ry = (-(m*(rx - self.x) + self.y)) % self.curve.p
    return Point(self.curve, rx, ry)

def double_and_add(self, k: int) -> Point:
    assert isinstance(k, int) and k >= 0
    result = INF
    append = self
    while k:
        if k & 1:
            result += append
        append += append
        k >>= 1
    return result


Point.__add__ = elliptic_curve_addition # monkey patch addition into the Point class
Point.__rmul__ = double_and_add # monkey patch double and add into the Point class for convenience

# "verify" correctness
# sk = 2
# pk = G + G
# print("secret key: ", sk, "public key: ", pk)
# print("Public key lies on the curve: ", (pk.y ** 2 - pk.x ** 3 - 7) % pk.curve.p == 0)

# sk = 5
# pk = G + G + G + G
# print("secret key: ", sk, "public key: ", pk)
# print("Public key lies on the curve: ", (pk.y ** 2 - pk.x ** 3 - 7) % pk.curve.p == 0)

# print(G == 1*G)
# print(G + G == 2*G)
# print(G + G + G == 3*G)
