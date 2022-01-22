from fnmatch import translate
from solcx import compile_standard, install_solc
import web3
import os

install_solc("0.6.0")
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our solidity

compiled_sol = compile_standard(
   {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                 "*": {"*": ["abi", "metadata", "evm.bytecode","evm.sourceMap"]}
            }
        }
   },
   solc_version="0.6.0",
)
# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
print(abi)

# for connecting to ganache
w3 = web3.Web3(web3.Web3.HTTPProvider("http://0.0.0.0:7545"))
chain_id = 1337
my_address = "0x233A704F1412293a3Ed075B682fA97e8d487124A"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi = abi, bytecode=bytecode)

# Get the latest transaction
nonce =  w3.eth.getTransactionCount(my_address)
print(nonce)
# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

# Build a transaction
transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId":chain_id, 
    "from":my_address, 
    "nonce": nonce
})

# Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key= private_key)

# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Transaction receipt / confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(signed_txn)

# Working with the contract, you always need
# Contract ABI
# Contract Address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value,but don't make a state change
# Transact -> It makes a state change
print(simple_storage.functions.retrieve().call()) #calling the retrieve function that don't make a state change

#Build transaction
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1 
    }
)

#Sign transaction
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key = private_key
)

#send transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())