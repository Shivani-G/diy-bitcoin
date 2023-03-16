from dataclasses import dataclass
from Script import Script

@dataclass
class TxIn:
	prev_tx: bytes # prev txn id- hash of prev txn contents
	prev_index: int # UTXO (Unspent Txn Output) output index in the transaction
	script_sig: Script = None # unlocking script goes here
	sequence: int = 0xffffffff # originally intended for "high frequency trades", with locktime
