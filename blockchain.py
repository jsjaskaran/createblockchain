# Create a Blockchain

# importing libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain:

	def __init__(self):
		self.chain = []
		self.create_block(proof = 1, prev_hash = '0') # create genesis block

	# create blocks
	# we use this fn. right after a block is mined
	# proof of work, previous hash
	def create_block(self, proof, prev_hash):
		block = {}
		block['index'] = len(self.chain) + 1
		block['timestamp'] = str(datetime.datetime.now())
		block['proof'] = proof
		block['previous_hash'] = prev_hash

		self.chain.append(block)
		return block

	# return last block of chain
	def get_previous_block(self):
		return self.chain[-1]

	def proof_of_work(self, prev_proof):
		new_proof = 1 # increment by 1 to find the right proof (solve by trial-error approach)
		check_proof = False

		while check_proof is False:
			# problem that miners have to solve, can make operation more complex for challenging problem
			hash_operation = hashlib.sha256(str(new_proof ** 2 - prev_proof ** 2).encode()).hexdigest()
			if hash_operation[:4] == '0000':
				check_proof = True
			else:
				new_proof += 1

		return new_proof

	# create a hash of the block
	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys = True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	# check if the chain is valid
	def is_chain_valid(self, chain):
		previous_block = chain[0]
		block_index = 1

		while block_index < len(chain):
			block = chain[block_index]
			# previous hash of this block is equal to hash of previous block
			if block['previous_hash'] != self.hash(previous_block):
				return False

			# check for proof of work
			previous_proof = previous_block['proof']
			proof = block['proof']

			hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
			if hash_operation[:4] != '0000':
				return False

			previous_block = block
			block_index += 1

		return True


# Part 2: Mining Blockchain

# create web app
app = Flask(__name__)

# blockchain
blockchain = Blockchain() # instance

# Mining block
@app.route('/mineblock', methods=['GET'])
def mine_block():
	previous_block = blockchain.get_previous_block()
	previous_proof = previous_block['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hash(previous_block)

	block = blockchain.create_block(proof, previous_hash)

	response = {}
	response['message'] = 'Congratulations, you just mined a block!'
	response['index'] = block['index']
	response['timestamp'] = block['timestamp']
	response['previous_hash'] = block['previous_hash']

	return jsonify(response), 200

@app.route('/getchain', methods=['GET'])
def get_blockchain():
	response = {}
	response['chain'] = blockchain.chain
	response['length'] = len(blockchain.chain)
	response['message'] = 'The current blockchain'

	return jsonify(response), 200

# running the app
app.run(host = '0.0.0.0', port = 5000)