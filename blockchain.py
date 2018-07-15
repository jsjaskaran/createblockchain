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