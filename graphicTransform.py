from PIL import Image
import math
import cv2

def main():
	# image = cv2.imread('scenery.jpeg')
	# gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	# canny = cv2.Canny(blurred, 30, 150)
	# cv2.imshow('Result - Canny', canny)
	# cv2.waitKey(0)


	im = Image.open("scenery.jpeg")
	# im = Image.open("blur.jpg")
	# im.show()

	### convert PNG to JPG
	# rgb_im = im.convert('RGB')
	# rgb_im.save('blur.jpg')
	
	# print im.format, im.size, im.mode
	print(str(im.format) + " / " + str(im.size) + " / " + str(im.mode))
	# Gray = R*0.299 + G*0.587 + B*0.114
	# GRAY = (R*299 + G*587 + B*114 + 500)/1000
	# GRAY = (R*30 + G*59 + B*11 + 50)/100
	# RGBtoGRAY(im)
	# im.close()
	# im = Image.open("scenery.jpeg")
	# softlightFilter(im)
	# im.close()
	# im = Image.open("scenery.jpeg")
	# rmRED(im)
	# im.close()
	# im = Image.open("scenery.jpeg")
	# inverted(im)
	# im.close()
	# im = Image.open("gray.png")
	
	blur(im)
	im.close()
	im2 = Image.open("blur.png")
	im2.show()
	im2.close()

	# contour(im)
	# im.save("contour.png", "PNG")
	# im.show()
	# im.close()
	
# im.show()


def contour(im):
	im_width, im_height = im.size
	threshold = 20
	pixels = im.load()
	pixels_new = im.load()
	flagArr = [[0 for x in range(im_height)] for y in range(im_width)]
	for i in range(im_width):
		for j in range(im_height):
			if(i>0 and j>0 and i<im_width-5 and j<im_height-5):
				r, g, b = pixels[i, j]
				r1=b1=g1=0
				for count in range(5):
					r1 = r1+pixels[i+count, j][0]*(5-count)
					g1 = g1+pixels[i+count, j][1]*(5-count)
					b1 = b1+pixels[i+count, j][2]*(5-count)
				r1 = r1/15
				g1 = g1/15
				b1 = b1/15
				# g1 = (pixels[i+1, j][1] + pixels[i+2, j][1] + pixels[i+3, j][1] + pixels[i+4, j][1] + pixels[i+5, j][1])/5
				# b1 = (pixels[i+1, j][2] + pixels[i+2, j][2] + pixels[i+3, j][2] + pixels[i+4, j][2] + pixels[i+5, j][2])/5
				r2=b2=g2=0
				for count in range(5):
					r2 = r2+pixels[i, j+count][0]*(5-count)
					g2 = g2+pixels[i, j+count][1]*(5-count)
					b2 = b2+pixels[i, j+count][2]*(5-count)
				r2 = r2/15
				g2 = g2/15
				b2 = b2/15

				# r2 = (pixels[i, j+1][0] + pixels[i, j+2][0] + pixels[i, j+3][0] + pixels[i, j+4][0] + pixels[i, j+5][0])/5
				# g2 = (pixels[i, j+1][1] + pixels[i, j+2][1] + pixels[i, j+3][1] + pixels[i, j+4][1] + pixels[i, j+5][1])/5
				# b2 = (pixels[i, j+1][2] + pixels[i, j+2][2] + pixels[i, j+3][2] + pixels[i, j+4][2] + pixels[i, j+5][2])/5
				
				if flagArr[i][j] != 1:
					if(abs(r-r1)>threshold or abs(g-g1)>threshold or abs(b-b1)>threshold):
						pixels_new[i, j] = (0,0,0)
						flagArr[i][j] = 1
					elif(abs(r-r2)>threshold or abs(g-g2)>threshold or abs(b-b2)>threshold):
						pixels_new[i, j] = (0,0,0)
						flagArr[i][j] = 1
					else:
						pixels_new[i, j] = (255, 255, 255)
	im.save("contour.png", "PNG")



def RGBtoGRAY(im):
	im_width, im_height = im.size
	pixels = im.load()
	for i in range(im_width):
		for j in range(im_height):
			r, g, b = pixels[i, j]
			gray = math.floor((r*30 + g*59 + b*11 + 50)/100)
			pixels[i,j] = (gray, gray, gray)
	im.save("gray.png", "PNG")

def softlightFilter(im):
	im_width, im_height = im.size
	pixels = im.load()
	for i in range(im_width):
		for j in range(im_height):
			r, g, b = pixels[i, j]
			r = 250 if r+30>250 else r+45
			g = 250 if g+30>250 else g+45
			b = 250 if b+30>250 else b+45
			pixels[i,j] = (r, g, b)
	im.save("softlightFilter.png", "PNG")

def blur(im):
	im_width, im_height = im.size
	pixels = im.load()
	pixels_new = im.load()
	for i in range(im_width):
		for j in range(im_height):
			if(i>0 and j>0 and i<im_width-1 and j<im_height-1):
				tmp_pixel = (0,0,0)
				for idx in range(-1,2):
					for idy in range(-1,2):
						tmp_pixel = (tmp_pixel[0] + pixels[i+idx,j+idy][0], tmp_pixel[1] + pixels[i+idx,j+idy][1], tmp_pixel[2] + pixels[i+idx,j+idy][2])
				pixels_new[i, j] = tuple(ele1 // ele2 for ele1, ele2 in zip(tmp_pixel, (9, 9, 9)))
				
				# r1, g1, b1 = pixels[i-1, j-1]
				# r2, g2, b2 = pixels[i, j-1]
				# r3, g3, b3 = pixels[i+1, j-1]
				# r4, g4, b4 = pixels[i-1, j]
				# r5, g5, b5 = pixels[i, j]
				# r6, g6, b6 = pixels[i+1, j]
				# r7, g7, b7 = pixels[i-1, j+1]
				# r8, g8, b8 = pixels[i, j+1]
				# r9, g9, b9 = pixels[i+1, j+1]

				# r = math.floor((r1+r2+r3+r4+r5+r6+r7+r8+r9)/9)
				# g = math.floor((g1+g2+g3+g4+g5+g6+g7+g8+g9)/9)
				# b = math.floor((b1+b2+b3+b4+b5+b6+b7+b8+b9)/9)
				# pixels_new[i, j] = (r, g, b)
			else:
				pixels_new[i, j] = pixels[i, j]
	
	im.save("blur.png", "PNG")


def rmRED(im):
	im_width, im_height = im.size
	pixels = im.load()
	for i in range(im_width):
		for j in range(im_height):
			r, g, b = pixels[i, j]
			r = 0 if (g < 60 and b < 60) else r
			g = 250 if g+30>250 else g+45
			b = 250 if b+30>250 else b+45
			pixels[i,j] = (r, g, b)
	im.save("removeRED.png", "PNG")

def inverted(im):
	im_width, im_height = im.size
	pixels = im.load()
	for i in range(im_width):
		for j in range(im_height):
			r, g, b = pixels[i, j]
			r = 255-r
			g = 255-g
			b = 255-b
			pixels[i,j] = (r, g, b)
	im.save("inverted.png", "PNG")

if __name__ == '__main__':
	main()
