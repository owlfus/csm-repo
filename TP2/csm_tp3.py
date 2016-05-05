import numpy as np
import jpeg_tables
import cv2


def read_image(name):
	return cv2.imread(name, cv2.CV_LOAD_IMAGE_GRAYSCALE)

def divide_image(image, size):
	num_lin_blocks = len(image[0])/size
	num_lin_extra = len(image[0])%size
	num_col_blocks = len(image[1])/size
	num_col_extra = len(image[1])%size

	print 'Num line blocks = ', num_lin_blocks, 'with extra ', num_lin_extra, ' line info'
	print 'Num column blocks = ', num_col_blocks, 'with extra ', num_col_extra, ' column info'
	
	if num_lin_extra != 0:
		for line in image:
			line = np.append(line, np.zeros(size - num_lin_extra))
	if num_col_extra != 0:
		for column in range(0, size - num_col_extra):
			image = np.append(image, np.zeros(image.shape[0]))

	blocks = []
	for lin in range(0, image.shape[0], size):
		for col in range(0, image.shape[1], size):
			block = []
			for i in range(0, size):
				block.append(image[lin:lin + size][i][col:col + size])
			blocks.append(block)
	return np.array(blocks)



###########################################################################################
#                                      MAIN PROGRAM
###########################################################################################
print "Program start."

img = read_image("lena_gray.tiff")

divided = divide_image(img, 8)

print divided[0]
#DCT_2D_CODE
#dct_code = cv2.dct(block)

#DCT_2D_DECODE
#dct_decode = cv2.dct(dct_code, [],cv2.DCT_INVERSE)


print "Program end."