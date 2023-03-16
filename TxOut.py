from dataclasses import dataclass
from Script import Script

@dataclass
class TxOut(object):
	amount: int # in units of satoshi (1BTC = 1e^-8 of a bitcoin)
	script_pubkey: Script = None # locking script
