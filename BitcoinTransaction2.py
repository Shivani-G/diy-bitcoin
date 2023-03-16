from Generator import bitcoin_gen
from PublicKey import PublicKey
from TxIn import TxIn
from TxOut import TxOut
from Tx import Tx, generate_script_sig
from BitcoinTransaction1 import wallet1, wallet2
from Script import Script
import random
from Signature import sign
from SHA256 import sha256

# create new wallet
sk = int.from_bytes(b'Shivani gonna get rich!', 'big')
assert 1 <= sk < bitcoin_gen.n
pk = sk*bitcoin_gen.G
add = PublicKey.from_point(pk).address(net='test', compressed=True)

wallet3 = {
	"secretKey": sk,
	"publicKey": pk,
	"address": add
}
print("wallet3: ", wallet3, end = "\n\n\n")

wallet3pkhash = PublicKey.from_point(wallet3["publicKey"]).encode(compressed=True, hash160=True)
print("wallet3pkhash: ", wallet3pkhash, wallet3pkhash.hex(), len(wallet3pkhash), end = "\n\n")
outscript = Script(
	cmds = [118, 169, wallet3pkhash, 136, 172]
)

tx_in1 = TxIn(
	prev_tx = bytes.fromhex('afd4928a600186136ec7faeca7416e9731973e9c0ae7f7681a9e8f5b322e5646'),
	prev_index = 0
)

tx_in2 = TxIn(
	prev_tx = bytes.fromhex('afd4928a600186136ec7faeca7416e9731973e9c0ae7f7681a9e8f5b322e5646'),
	prev_index = 1
)

tx_out = TxOut(
	amount = 9121 # txn fee = 1.1sat/B, txn fee has to be greater than min relay fee which is length of message, 338 in this case
)

wallet2_pk_hash = PublicKey.from_point(wallet2["publicKey"]).encode(compressed=True, hash160=True)
prev_out1_pubkey_script = Script(
	cmds = [118, 169, wallet2_pk_hash, 136, 172]
)
tx_in1.prev_tx_script_pubkey = prev_out1_pubkey_script

wallet1_pk_hash = PublicKey.from_point(wallet1["publicKey"]).encode(compressed=True, hash160=True)
prev_out2_pubkey_script = Script(
	cmds = [118, 169, wallet1_pk_hash, 136, 172]
)
tx_in2.prev_tx_script_pubkey = prev_out2_pubkey_script

tx_out.script_pubkey = outscript

tx = Tx(
	version = 1,
	tx_ins = [tx_in1, tx_in2],
	tx_outs = [tx_out]
)


message1 = tx.encode(sig_index = 0)
print("message1: ", message1)
random.seed(int.from_bytes(sha256(message1), 'big')) # see note below
sig1 = sign(wallet2["secretKey"], message1)

message2 = tx.encode(sig_index = 1)
print("message2: ", message2)
random.seed(int.from_bytes(sha256(message2), 'big')) # see note below
sig2 = sign(wallet1["secretKey"], message2)

tx_in1.script_sig = generate_script_sig(sig1.encode(), wallet2["publicKey"])
tx_in2.script_sig = generate_script_sig(sig2.encode(), wallet1["publicKey"])

print("Complete transaction: ", tx)
print("Complete transaction in hexadecimal: ", tx.encode().hex(), len(tx.encode()))
print(tx.id()) # once this transaction goes through, this will be its id

