from CurveUtil import Point
from Generator import bitcoin_gen
from PublicKey import PublicKey
from Script import Script
from Tx import Tx, generate_script_sig
from TxIn import TxIn
from TxOut import TxOut
from Signature import sign
import random
from SHA256 import sha256

# create src and destination wallets
sk = int.from_bytes(b'Shivani is the best!', 'big')
assert 1 <= sk < bitcoin_gen.n
pk = sk*bitcoin_gen.G
add = PublicKey.from_point(pk).address(net='test', compressed=True)

wallet1 = {
	"secretKey": sk,
	"publicKey": pk,
	"address": add
}

sk = int.from_bytes(b'Shivani is still the best!', 'big')
assert 1 <= sk < bitcoin_gen.n
pk = sk*bitcoin_gen.G
add = PublicKey.from_point(pk).address(net='test', compressed=True)

wallet2 = {
	"secretKey": sk,
	"publicKey": pk,
	"address": add
}
print("wallet1: ", wallet1, end = "\n\n")
print("wallet2: ", wallet2, end = "\n\n\n")


wallet1pkhash = PublicKey.from_point(wallet1["publicKey"]).encode(compressed=True, hash160=True)
print("wallet1pkhash: ", wallet1pkhash, wallet1pkhash.hex(), len(wallet1pkhash), end = "\n\n")
out2script = Script(
	cmds = [118, 169, wallet1pkhash, 136, 172]
)
print("out2script: ", out2script.encode().hex(), end = "\n\n")

wallet2pkhash = PublicKey.from_point(wallet2["publicKey"]).encode(compressed=True, hash160=True)
print("wallet2pkhash: ", wallet2pkhash, wallet2pkhash.hex(), len(wallet2pkhash), end = "\n\n")
out1script = Script(
	cmds = [118, 169, wallet2pkhash, 136, 172]
)
print("out1script: ", out1script.encode().hex(), end = "\n\n\n")

tx_in = TxIn(
	prev_tx = bytes.fromhex('2716d6fad23ae7688a317e4c0d06391adde0b304362e834f85b54e4083f096b8'),
	prev_index = 1,
	script_sig = None
)
tx_in.prev_tx_script_pubkey = out2script # this is used in place of sig_script in tx_in to produce the sig_script

tx_out1 = TxOut(
	amount = 5000
)

tx_out2 = TxOut(
	amount = 4500 # txn fee = 2sat/B
)
tx_out1.script_pubkey = out1script
tx_out2.script_pubkey = out2script

tx = Tx(
    version = 1,
    tx_ins = [tx_in],
    tx_outs = [tx_out1, tx_out2],
)
print("Decoded(deserialized) transaction: ", tx, end = "\n\n")

message = tx.encode(sig_index = 0)
print("Encoded(serialized) transaction", message.hex(), end = "\n\n")

random.seed(int.from_bytes(sha256(message), 'big')) # see note below
sig = sign(wallet1["secretKey"], message)
print("digital signature to be used in unlocking script", sig, end = "\n\n")
sig_bytes = sig.encode()
print("Encoded digital signature: ", sig_bytes.hex(), end = "\n\n\n")
tx_in.script_sig = generate_script_sig(sig_bytes, wallet1["publicKey"])

print("Fully constructed transaction and in encoded form: ", tx, tx.encode(), end = "\n\n")
print("Transaction hex(to be broadcasted to bitcoin nodes) and length: ", tx.encode().hex(), len(tx.encode()))

print(tx.id()) # once this transaction goes through, this will be its id
