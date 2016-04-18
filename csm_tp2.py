# Author - Tomaz Azinhal - 41619

import matplotlib.pyplot as plt
import numpy as np
import operator
from node import Node
import cv2

"""
Sorts the string into an array.
Keeps duplicate values together.
"""
def sort_to_array(word):
	arr = np.array(list(word))
	arr.sort()
	return arr

"""
For each symbol in a word, counts the number of occurrences of that symbol.
Returns two arrays.
One array has the symbols. The other has the number of occurrences.
"""
def make_dicionary(word):
	temp = word
	size = len(word)
	set(temp)
	amount = np.array([], np.int8)
	for symbol in temp:
		amount = np.append(amount, sum(word == symbol))
	return temp, amount

"""
Runs the Huffman Algorythm for the given symbols and occurrences.
For each pair with smallest occurrences, joins the two and creates a node.
Reorders the tree by highest to lowest occurrences and repeats until there is only one node.
"""
def huffman(array):
	nodes = transform_tree(array)
	tree = make_tree(nodes)
	table = make_table(tree, array)
	return table

"""
Creates the table that for each symbol will code into a series of bits.
"""
def make_table(tree, symbols):
	table = np.array([])
	for symbol in symbols:
		sym, code = tree.search(symbol[0])
		table = np.append(table, np.array([sym, code]))
	return table
	
"""
Searches given tree for symbol
"""
	

"""
Creates the Huffman tree with codes for each symbol.
"""
def make_tree(tree):
	while(len(tree) > 1):
		nodes = tree[-2:]
		tree = tree[:-2]
		new_node = Node()
		new_node.set_children(nodes[0], nodes[1])
		tree = np.append(tree, new_node)
		arr = sort_by_freq(tree)
		tree = transform_tree(arr)
	root = tree[0]
	root.expand('')
	return root

"""
Sorts the current Huffman tree by each node's frequency.
"""
def sort_by_freq(tree):
	return sorted(tree, key=lambda node:node.freq, reverse=True)

"""
Transforms the Huffman container into an array of nodes.
"""
def transform_tree(array):
	if isinstance(array[0], tuple):
		tree = np.array([])
		for tupl in array:
			n = Node()
			n.set_name(tupl[0])
			n.set_freq(tupl[1])
			tree = np.append(tree, n)
	else :
		tree = np.array(array)
	return tree

"""
Turns two arrays into a dictionary.
Sorts the diccionary into an array of tuples 
sorted by highest to lowest occurrences.
"""
def sort_to_dict(keys, values):
	dicc = dict(zip(keys, values))
	return sorted(dicc.items(), key=operator.itemgetter(1), reverse=True) #True = Highest 2 Lowest
																		   #False = Lowest 2 Highest

"""
Reads the image with the name into an array.
"""
def read_image(name):
	img = cv2.imread(name)
	print('Image "', img, '" read.')

"""
Writes an image with the name.
"""
def write_image(name, image):
	pass



###########################################################################################
#                                      MAIN PROGRAM
###########################################################################################
print "Program start."

# img = read_image("lena_gray.tiff")
word = "ilikestrings"
array = sort_to_array(word)
S, P = make_dicionary(array)
D = sort_to_dict(S, P)
tree = huffman(D)

print "Program end."
