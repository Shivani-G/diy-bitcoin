from Curve import Curve, bitcoin_curve
from dataclasses import dataclass

@dataclass
class Point(object):
	"""docstring for Point"""
	curve: Curve
	x: int
	y: int

G = Point(
	curve = bitcoin_curve,
	x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
	y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
)

# print("Verifying Generator point is on the curve secp256k1: ", (G.y ** 2 - G.x ** 3 - 7) % G.curve.p == 0 )


import random
random.seed(1337)
x = random.randrange(0, bitcoin_curve.p)
y = random.randrange(0, bitcoin_curve.p)
R = Point(
	curve = bitcoin_curve,
	x = x,
	y = y
)
# print("Verifying some totally random point is (mostly) not on the curve secp256k1: ", (R.y ** 2 - R.x ** 3 - 7) % R.curve.p == 0 )