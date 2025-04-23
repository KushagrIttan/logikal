import hashlib
from time import time
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash_value):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash_value

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = self.create_block(data="Genesis Block", previous_hash="0")
        self.chain.append(genesis_block)

    def create_block(self, data, previous_hash):
        index = len(self.chain)
        timestamp = time()
        hash = self.hash_block(index, previous_hash, timestamp, data)
        return Block(index, previous_hash, timestamp, data, hash)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = self.create_block(data, previous_block.hash)
        self.chain.append(new_block)

    def hash_block(self, index, previous_hash, timestamp, data):
        block_string = f"{index}{previous_hash}{timestamp}{data}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.hash_block(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

def shipping_data():
    with open('jsons/shipment_data.json', 'r') as json_file:
        shipment_data = json.load(json_file)
    blockchain = Blockchain()
    blockchain.add_block(shipment_data)

    # for block in blockchain.chain:
    #     print(f"Index: {block.index}")
    #     print(f"Previous Hash: {block.previous_hash}")
    #     print(f"Timestamp: {block.timestamp}")
    #     print(f"Data: {block.data}")
    #     print(f"Hash: {block.hash}")
    #     print("\n")
    #
    # print("Is blockchain valid?", blockchain.is_chain_valid())