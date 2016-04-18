# Author - Tomaz Azinhal - 41619
import numpy as np

class Node(object):
	name = ""
	freq = 0
	left = None
	right = None
	code = ""

	"""
	Constructor.
	"""
	def __init__(self):
		pass

	"""
	Sets the name of the node.
	"""
	def set_name(self, name):
		self.name = name

	"""
	Sets the freq of the node.
	"""
	def set_freq(self, freq):
		self.freq = freq

	"""
	Sets the children of the node.
	"""
	def set_children(self, ln, rn):
		self.name = ln.name + rn.name
		self.freq = ln.freq + rn.freq
		self.left = ln 
		self.right = rn

	"""
	Prints node. Used for debugging.
	"""
	def to_string(self):
		if self.left is None: 
			print (self.name, self.freq)
		else :
			print (self.name, self.freq, self.left.name, self.right.name)

	"""
	Expands node and all the subsequent nodes and completes codes for each node.
	"""
	def expand(self, code):
		if (len(self.name) == 1):
			self.code = code
			return
		else:
			self.right.expand(code + '1')
			self.left.expand(code + '0')

	"""
	Searches if the given node has the symbol and returns its code.
	"""
	def search(self, symbol):
		pass