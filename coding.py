import numpy as np
import cv2
import sys

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
	sh = img.shape
	txt = np.ones(shape=sh)
	# cv2.imshow("blank", txt)

	fontface = cv2.FONT_HERSHEY_SIMPLEX
	fontscale = 1
	thickness = 2
	color = (0, 0, 0)
	orig = (10, 100)
	linetype = cv2.LINE_AA
	txt1 = cv2.putText(txt, text, orig, fontface, fontscale, color, thickness, linetype)
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
	inp = sys.argv
	img = None
	text = None
	if len(inp) == 4:
		if inp[1] == "encode":
			try:
				filename = inp[2]
				img = cv2.imread(filename)
				text = inp[3]
			except FileNotFoundError:
				print("File does not exist.")
				exit(0)
			new_img = encoder(img, text)
			tst = decoder(new_img)
			cv2.imshow("in enc", tst)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
			tmp = filename.split(".")
			new_filename = tmp[0]+"_encoded.png"	# This is important. Doesn't work if image saved as jpg
			cv2.imwrite(new_filename, new_img)

			print(new_filename)
			tst2 = cv2.imread(new_filename)
			tst2 = decoder(tst2)
			cv2.imshow("in enc", tst2)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
			print("Successfully encoded")
		else:
			print("Invalid command")

	elif len(inp) == 3:
		if inp[1] == "decode":
			try:
				filename = inp[2]
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



