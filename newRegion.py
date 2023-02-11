from common import *
import numpy as np
import cv2 as cv
import pytesseract

from ocr3 import countSubstatLines


## this looks good
left, top = 1386, 435
width, height = 245, 21
extraSpace = 5

newSubstatRegion = (left - extraSpace, top - extraSpace, width + extraSpace * 2, height + extraSpace * 2)


if __name__ == '__main__':
	video = cv.VideoCapture('2023-01-15 17-48-41.mp4')
	for frameObj in iterateVideo(video):
		if frameObj['index'] % 5 != 0: continue
		img = crop(frameObj['img'], newSubstatRegion)
		print(pytesseract.image_to_string(img))
		cv.imshow('test', img)
		cv.waitKey(1)