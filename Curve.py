from dataclasses import dataclass

@dataclass
class Curve(object):
	"""
	Elliptic curve over the field of integers modulo prime p
	Points on the curve satisfy y^2 = x^3 + a*x + b (mod p)
	"""
	p: int # the prime modulus of the finite field
	a: int
	b: int

"""
secp256k1 uses a = 0, b = 7, so we are dealing with the curve: y^2 = x^3 + 7 (mod p)
"""
bitcoin_curve = Curve(
	p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
	a = 0x0000000000000000000000000000000000000000000000000000000000000000,
	b = 0x0000000000000000000000000000000000000000000000000000000000000007
)
# print(bitcoin_curve)
		