import numpy as np
import cv2
import textwrap
import argparse

def split(img):
	l = []
	for i in range(8):
		l.append(img%2)
		img = img//2
	return l


def merge(l):
	img = l[0]
	for i in range(1, 8):
		img += (2**i)*l[i]
	return img


def get_text(img, text):
	factor = 1/20
	text = textwrap.wrap(text, width=len(img[0])*factor)
	sh = img.shape
	txt = np.ones(shape=sh)
	
	fontface = cv2.FONT_HERSHEY_SIMPLEX
	fontscale = 0.7
	thickness = 2	
	color = (0, 0, 0)
	x = 10
	y = 20
	orig = (x, y)
	linetype = cv2.LINE_AA
	for i in text:
		txt1 = cv2.putText(txt, i, orig, fontface, fontscale, color, thickness, linetype)
		orig = (orig[0], orig[1]+30)
	txt2 = txt1 // 255
	txt2 = txt.astype("uint8")
	return txt2






def encoder(image, text, bitplane=0):
	txt = get_text(image, text)

	bitmap = split(image)
	frames = []
	# frames.append(txt)
	for i in range(0, 8):
		frames.append(bitmap[i])
	frames[bitplane] = txt
	new_image = merge(frames)

	return new_image


def decoder(image):
	try:
		bitmap = split(image)
		code = bitmap[0] * 255
		return code
	except TypeError:
		print("Invalid image")



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--action", required=True)
	parser.add_argument("-i", "--image", required=True)
	parser.add_argument("-t", "--text", nargs="+")
	args = parser.parse_args()

	img = None
	text = None
	if args.action == "encode":
		try:
			filename = args.image
			img = cv2.imread(filename)
			text = ' '.join(args.text)
		except FileNotFoundError:
			print("File does not exist.")
			exit(0)
		new_img = encoder(img, text)
		tmp = filename.split(".")
		new_filename = tmp[0]+"_encoded.png"	# This is important. Doesn't work if image saved as jpg
		cv2.imwrite(new_filename, new_img)
		print("Successfully encoded")
		

	elif args.action == "decode":
		try:
			filename = args.image
			img = cv2.imread(filename)
		except FileNotFoundError:
			print("File does not exist.")
			exit(0)
		new_img = decoder(img)
		cv2.imshow("decoded", new_img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		tmp = filename.split(".")
		new_filename = tmp[0]+"_decoded."+tmp[1]
		cv2.imwrite(new_filename, new_img)
		print("Successfully decoded")


