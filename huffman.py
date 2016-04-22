# Author - Tomaz Azinhal - 41619

from file_manager import File_Manager
import matplotlib.pyplot as plt
from node import Node
from leaf import Leaf
import numpy as np
import operator
import cv2

"""
TODO
"""
def get_image(name):
	x = cv2.imread(name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
	x = x.ravel()
	return x
"""
TODO
"""
def get_symbols_and_occurrences(image):
	h, bins, patches = plt.hist(image, 256, [0, 256])
	h = np.array(h, np.int16)
	bins = np.array(bins, np.int16)
	return bins[:-1], h

"""
TODO
"""
def get_tuple_array(keys, values):
	dicc = dict(zip(keys, values))
	return sorted(dicc.items(), key=operator.itemgetter(1), reverse=True) #True = Highest 2 Lowest
																		   #False = Lowest 2 Highest

"""
TODO
"""
def get_huffman(table):
	tree = transform_tree(table)
	root = make_tree(tree)
	return root

"""
TODO
"""
def transform_tree(array):
	if isinstance(array[0], tuple):
		tree = np.array([])
		for tupl in array:
			l = Leaf()
			l.set_name(tupl[0])
			l.set_freq(tupl[1])
			tree = np.append(tree, l)
	else :
		tree = np.array(array)
	return tree

"""
TODO
"""
def make_tree(tree):
	temp = tree
	while(len(tree) > 1):
		leaves = tree[-2:]
		tree = tree[:-2]
		leaf = Leaf()
		leaf.set_children(leaves[0], leaves[1])
		tree = np.append(tree, leaf)
		arr = sort_by_freq(tree)
		tree = transform_tree(arr)
	root = tree[0]
	root.expand('')
	return root, temp

"""
Sorts the Leaf array by its frequency.
"""
def sort_by_freq(tree):
	return sorted(tree, key=lambda leaf:leaf.freq, reverse=True)

"""
For the value in each pixel, gets the bits that codify that value from the dictionary.
"""
def codify(img, dicc):
	result = ''
	for index in img:
		result += dicc[index]
	return result

"""
Checks if the bits are in the dictionary, if they are, then get the symbol.
"""
def decodify(code, dicc):
	reverse_dicc = dict(zip(dicc.values(), dicc.keys()))
	result = np.array([])
	start_index = 0
	for end_index in range(len(code) + 1):
		c = ''
		try:
			symbol = reverse_dicc[code[start_index:end_index]]
			result = np.append(result, symbol)
			start_index = end_index
		except KeyError:
			continue
	print 'Code Length = ', len(code)
	return result


###########################################################################################
#                                      MAIN PROGRAM
###########################################################################################
print "Program start."

img = get_image('lena_gray.tiff')
img = get_image('c.jpg')

S, H = get_symbols_and_occurrences(img)
D = get_tuple_array(S, H)
Tree, Code = get_huffman(D)

keys = [c.name[0] for c in Code]
values = [c.code for c in Code]
dicc = dict(zip(keys, values))

img_code = codify(img, dicc)

img_decode = decodify(img_code, dicc)

for x in sorted(Code, key=lambda leaf:leaf.name[0], reverse=True):
	print x.name[0], ' - ', x.freq, ' - ', x.code

poop = img_decode == img
print 'Number of Fake pixels = ', sum(poop == False)

manager = File_Manager('test')
manager.write_file(img_code)
print 'Image Written.'
file = manager.read_file()
print file

print "Program end."