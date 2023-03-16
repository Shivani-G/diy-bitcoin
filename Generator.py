from dataclasses import dataclass
from Point import Point, G

@dataclass
class Generator(object):
	"""A Generator over a curve and the (pre-computed) order"""
	G: Point # generator point on the curve
	n: int   # the order of the curve- total no of points on the curve

bitcoin_gen = Generator(
	G = G,
	n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
)
# print(bitcoin_gen)
		