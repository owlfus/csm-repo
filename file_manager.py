# Author - Tomaz Azinhal - 41619
import binascii

class File_Manager(object):
	name = ''
	file = None

	def __init__(self, name):
		self.name = name + '.txt'

	def read_file(self):
		self.file = open(self.name, 'r')
		content = self.file.read()
		content = int(binascii.hexlify(content))
		content = bin(content)[2:]
		self.file.close()
		return content

	def write_file(self, content):
		self.file = open(self.name, 'w')
		temp = str(int(content, 2))
		if ((len(temp) % 2) > 0):
			temp = '0' + temp
		temp = binascii.unhexlify(temp)
		self.file.write(temp)
		self.file.close()