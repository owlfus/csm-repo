class File_Manager(object):
	name = ''
	file = None

	def __init__(self, name):
		self.name = name + '.txt'

	def read_file(self):
		self.file = open(self.name, 'r')
		content = self.file.read()
		return content

	def write_file(self, content):
		self.file = open(self.name, 'w')
		self.file.write(content)
		self.file.close()