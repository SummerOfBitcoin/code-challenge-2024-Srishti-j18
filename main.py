import os
import json
import hashlib
import time

# Constants
DIFFICULTY_TARGET = "0000ffff00000000000000000000000000000000000000000000000000000000"
BLOCK_SIZE_LIMIT = 1000000  # Maximum block size in bytes

# Function to read transactions from mempool JSON files
def read_transactions_from_mempool():
    transactions = []
    mempool_dir = "mempool"
    for filename in os.listdir(mempool_dir):
        if filename.endswith(".json"):
            with open(os.path.join(mempool_dir, filename), "r") as file:
                data = json.load(file)
                transactions.append(data)
    return transactions

# Function to validate transactions
def validate_transactions(transactions):
    valid_transactions = []
    invalid_transactions = []

    # Perform basic validation for demonstration purposes
    for tx in transactions:
        if is_valid_transaction(tx):
            valid_transactions.append(tx)
        else:
            invalid_transactions.append(tx)

    return valid_transactions, invalid_transactions

# Function to check if a transaction is valid (basic validation)
def is_valid_transaction(tx):
    # Perform basic validation by checking if transaction data is present
    return "txid" in tx and "inputs" in tx and "outputs" in tx

# Function to construct coinbase transaction
def construct_coinbase_transaction():
    # For simplicity, create a coinbase transaction with a single output
    coinbase_tx = {
        "txid": "coinbase",
        "inputs": [],
        "outputs": [{"address": "miner_address", "value": 50}]
    }
    return coinbase_tx

# Function to construct block
def construct_block(valid_transactions, coinbase_tx):
    # Include coinbase transaction in the list of transactions
    transactions = [coinbase_tx] + valid_transactions

    # Calculate Merkle root
    merkle_root = calculate_merkle_root(transactions)

    # Assemble block data
    block_data = {
        "transactions": transactions,
        "merkle_root": merkle_root,
        "timestamp": int(time.time()),
        "difficulty_target": DIFFICULTY_TARGET,
        "nonce": 0
    }

    return block_data

# Function to calculate Merkle root
def calculate_merkle_root(transactions):
    # Simplified version: Concatenate transaction IDs and hash repeatedly until only one hash remains
    transaction_ids = [tx["txid"] for tx in transactions]
    while len(transaction_ids) > 1:
        next_level = []
        for i in range(0, len(transaction_ids), 2):
            tx1 = transaction_ids[i]
            tx2 = transaction_ids[i + 1] if i + 1 < len(transaction_ids) else tx1
            combined = tx1 + tx2
            hashed = hashlib.sha256(combined.encode()).hexdigest()
            next_level.append(hashed)
        transaction_ids = next_level
    return transaction_ids[0]

# Function to mine block
def mine_block(block):
    # Mine the block by incrementing nonce until hash meets difficulty target
    while True:
        block_hash = calculate_block_hash(block)
        if block_hash < DIFFICULTY_TARGET:
            break
        block["nonce"] += 1
    return block

# Function to calculate block hash
def calculate_block_hash(block):
    block_string = json.dumps(block, sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()

# Function to write output to output.txt
def write_output(block_header, coinbase_tx, transaction_ids):
    with open("output.txt", "w") as f:
        # Write block header
        f.write(block_header + "\n")
        
        # Serialize coinbase transaction and write it
        coinbase_tx_serialized = json.dumps(coinbase_tx)
        f.write(coinbase_tx_serialized + "\n")

        # Write transaction IDs of mined transactions
        for txid in transaction_ids:
            f.write(txid + "\n")

# Main function
def main():
    # Read transactions from mempool
    transactions = read_transactions_from_mempool()

    # Validate transactions
    valid_transactions, _ = validate_transactions(transactions)

    # Construct coinbase transaction
    coinbase_tx = construct_coinbase_transaction()

    # Construct block
    block = construct_block(valid_transactions, coinbase_tx)

    # Mine block
    mined_block = mine_block(block)

    # Extract relevant data for output
    block_header = {
        "merkle_root": mined_block["merkle_root"],
        "timestamp": mined_block["timestamp"],
        "difficulty_target": mined_block["difficulty_target"],
        "nonce": mined_block["nonce"]
    }
    transaction_ids = [tx["txid"] for tx in mined_block["transactions"]]

    # Write output to output.txt
    write_output(json.dumps(block_header), coinbase_tx, transaction_ids)

# Execute main function
if __name__ == "__main__":
    main()
