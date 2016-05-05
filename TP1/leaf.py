# Author - G11

import numpy as np

class Leaf(object):
	name = np.array([], np.int32)
	freq = long
	left = None
	right = None
	code = ""

	"""
	Constructor.
	"""
	def __init__(self):
		pass

	"""
	Sets the name of the leaf.
	"""
	def set_name(self, name):
		self.name = np.array([name], np.int32)

	"""
	Sets the freq of the leaf.
	"""
	def set_freq(self, freq):
		self.freq = freq

	"""
	Sets the children of the leaf.
	"""
	def set_children(self, ln, rn):
		self.name = np.append(self.name, ln.name)
		self.name = np.append(self.name, rn.name)
		self.freq = np.int32 (ln.freq + rn.freq)
		self.left = ln
		self.right = rn


	"""
	Expands leaf and all the subsequent leaves and completes codes for each leaf.
		Expanding: 
			If the name is a symbol, 
			then atributes to self the code passed down from previous expasions.
			Else will expand right and left.
			Left is '0', Right is '1'.
	"""
	def expand(self, code):
		if (len(self.name) == 1):
			self.code = code
			return
		else:
			self.right.expand(code + '1')
			self.left.expand(code + '0')