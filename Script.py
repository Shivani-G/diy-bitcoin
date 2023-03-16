from dataclasses import dataclass
from typing import List, Union

def encode_int(i, nbytes, encoding = 'little'):
	""" encode integer i into nbytes bytes using a given byte ordering """
	return i.to_bytes(nbytes, encoding)

# varint as we dont know how many bytes to encode in. Also the first byte are constants for certain range of nos probably for easy decompressing
def encode_varint(i):
	""" encode a (possibly but rarely large) integer into bytes with a super simple compression scheme """
	if i < 0xfd: # i < 253
		return bytes([i])
	elif i < 0x10000: # i in btw 254 and 16^4
		return b'\xfd' + encode_int(i, 2) # return 253 in bytes + encode i in 2 bytes
	elif i < 0x100000000:
		return b'\xfe' + encode_int(i, 4) # return 254 in bytes + encode i in 4 bytes
	elif i < 0x10000000000000000:
		return b'\xff' + encode_int(i, 8) # return 255 in bytes + encode i in 8 bytes
	else:
		raise ValueError("integer too large: %d" % (i, ))

@dataclass
class Script(object):
	cmds: List[Union[int, bytes]]
	def encode(self):
		out = []
		for cmd in self.cmds:
			if isinstance(cmd, int):
				# opcodes like OP_DUP, OP_HASH160, etc are represented by integers; encode as a single byte
				out.append(encode_int(cmd, 1))
			elif isinstance(cmd, bytes):
				# bytes represent an element, encode its length and then content
				assert len(cmd) < 75 # any longer than this requires a bit of tedious handling that we'll skip here
				out.extend([encode_int(len(cmd), 1), cmd])

		ret = b''.join(out)
		return encode_varint(len(ret)) + ret


