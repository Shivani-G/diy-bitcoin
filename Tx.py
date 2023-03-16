from dataclasses import dataclass
from typing import List
from Script import encode_int, encode_varint
from TxIn import TxIn
from TxOut import TxOut
from PublicKey import PublicKey
from Script import Script
from SHA256 import sha256

@dataclass
class Tx:
	version: int
	tx_ins: List[TxIn]
	tx_outs: List[TxOut]
	locktime: int = 0

	def encode(self, sig_index = -1) -> bytes:
		out = []
		out.append(encode_int(self.version, 4))
		out.append(encode_varint(len(self.tx_ins)))
		if sig_index == -1:
			out.extend([tx_in.encode() for tx_in in self.tx_ins])
		else:
			out.extend([tx_in.encode(script_override = (i == sig_index)) for i, tx_in in enumerate(self.tx_ins)])
		out.append(encode_varint(len(self.tx_outs)))
		out.extend([tx_out.encode() for tx_out in self.tx_outs])
		out.append(encode_int(self.locktime, 4))
		out.append(encode_int(1, 4) if sig_index != -1 else b'') # 1 = 
		return b''.join(out)

	def id(self) -> str:
		return sha256(sha256(self.encode()))[::-1].hex() # little/big endian conventions require byte order swap



# we also need to know how to encode TxIn. This is just serialization protocol.
def txin_encode(self, script_override=None):
    out = []
    out += [self.prev_tx[::-1]] # little endian vs big endian encodings... sigh
    out += [encode_int(self.prev_index, 4)]

    if script_override is None:
        # None = just use the actual script
        out += [self.script_sig.encode()]
    elif script_override is True:
        # True = override the script with the script_pubkey of the associated input
        out += [self.prev_tx_script_pubkey.encode()]
    elif script_override is False:
        # False = override with an empty script
        out += [Script([]).encode()]
    else:
        raise ValueError("script_override must be one of None|True|False")

    out += [encode_int(self.sequence, 4)]
    return b''.join(out)

TxIn.encode = txin_encode # monkey patch into the class

# and TxOut as well
def txout_encode(self):
    out = []
    out += [encode_int(self.amount, 8)]
    out += [self.script_pubkey.encode()]
    return b''.join(out)

TxOut.encode = txout_encode # monkey patch into the class

def generate_script_sig(sig_bytes, public_key):
	# Append 1 (= SIGHASH_ALL), indicating this DER signature we created encoded "ALL" of the tx (by far most common)
	sig_bytes_and_type = sig_bytes + b'\x01'

	# Encode the public key into bytes. Notice we use hash160=False so we are revealing the full public key to Blockchain
	pubkey_bytes = PublicKey.from_point(public_key).encode(compressed=True, hash160=False)

	# Create a lightweight Script that just encodes those two things!
	script_sig = Script([sig_bytes_and_type, pubkey_bytes])

	return script_sig

