# Author - Tomaz Azinhal - 41619

from file_manager import File_Manager
import matplotlib.pyplot as plt
from time import time
from leaf import Leaf
import numpy as np
import operator
import cv2

"""
Reads an image, transforming into grayscale.
Afterwards ravels the array that can be analised by the next algorythm.
"""
def get_image(name):
	x = cv2.imread(name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
	x = x.ravel()
	return x
"""
From an image, will return all the existing symbols and the frequency of each one.
"""
def get_symbols_and_occurrences(image):
	h, bins, patches = plt.hist(image, 256, [0, 256])
	h = np.array(h, np.int16)
	bins = np.array(bins, np.int16)
	return bins[:-1], h

"""
Returns a list of tuples with they keys and values ordered by the highest to lowest value.
"""
def get_tuple_array(keys, values):
	dicc = dict(zip(keys, values))
	return sorted(dicc.items(), key=operator.itemgetter(1), reverse=True) #True = Highest 2 Lowest
																		   #False = Lowest 2 Highest

"""
Creates Huffman tree and returns its root.
This root contains all leaves and branches which contain the codes for all symbols.
"""
def get_huffman(table):
	tree = transform_tree(table)
	root = make_tree(tree)
	return root

"""
It will adapt the container of the tree.
If the parameter is a tuple with the symbols and its occurrences, 
then will create an array of leaves with the needed atributes.
If the parameter is a list, then it should be of leaves and 
must be converted to an array.
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
From a given array with leaves, removes the last 2 leaves, 
which should be the ones with the least occurrences.
It will then combine them and add this new symbol to the tree.
Afterwards, it will reorder the array by frequency and repeat this process.
When there is only one leaf, it means it is the word.
Then this root will be expanded in a way that each leaf will be given its code.
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
def decodify(code, dicc, image_length):
	reverse_dicc = dict(zip(dicc.values(), dicc.keys()))
	#result = np.array([])
	result = np.zeros(image_length)
	array_index = 0
	start_index = 0
	for end_index in range(len(code) + 1):
		c = ''
		try:
			symbol = reverse_dicc[code[start_index:end_index]]
			#result = np.append(result, symbol)
			result[array_index] = symbol
			array_index += 1
			start_index = end_index
		except KeyError:
			continue
	print '[Length] Code = ', len(code)
	return result

"""
Print the table in a pleasant way.
"""
def print_table(table):
	for x in sorted(table, key=lambda leaf:leaf.name[0], reverse=True):
		print x.name[0], ' - ', x.freq, ' - ', x.code



###########################################################################################
#                                      MAIN PROGRAM
###########################################################################################
print "Program start."


img = get_image('lena_gray.tiff')
# img = get_image('c.jpg')

manager = File_Manager('test')

S, H = get_symbols_and_occurrences(img)
D = get_tuple_array(S, H)

t0 = time()
Tree, Code = get_huffman(D)
t1 = time()

#print_table(Code)

print '[Time] Huffman = ', t1 - t0

keys = [c.name[0] for c in Code]
values = [c.code for c in Code]
dicc = dict(zip(keys, values))

t0 = time()
img_code = codify(img, dicc)
t1 = time()
print '[Time] Codify = ', t1 - t0

t0 = time()
manager.write_file(img_code)
t1 = time()
print '[Time] Image Write = ', t1 - t0


t0 = time()
file = manager.read_file()
t1 = time()
print '[Time] Image Read = ', t1 - t0

""" Decodify timer. Remove comment to show."""
t0 = time()
img_decode = decodify(file, dicc, len(img))
t1 = time()
print '[Time] Decodify = ', t1 - t0
#"""

""" Number of Fakes. Remove comment to show."""
fake_sum = img_decode == img
print 'Number of Fake pixels = ', sum(fake_sum == False)
#"""

total = sum(H)
entropy = 0
average = 0
for c in Code:
	pi = float(c.freq)/total
	if pi != 0:
		entropy += pi * np.log2(float(1)/pi)
		average += pi * len(c.code)
		
print 'Entropy = ', entropy

print 'Average bit size = ', average

print 'Eficiency = ', entropy / average

print "Program end."