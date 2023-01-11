import json
import cv2 as cv

def loadJsonFile(filename):
	f = open(filename)
	obj = json.load(f)
	f.close()
	return obj

def show(img):
	winName = "preview"
	cv.imshow(winName, img)
	cv.waitKey()
	cv.destroyWindow(winName)

def rect2slices(rect):
	xSlice = slice(rect[0], rect[0] + rect[2])
	ySlice = slice(rect[1], rect[1] + rect[3])
	return ySlice, xSlice

def crop(img, rect):
	return img[*rect2slices(rect)]

def binarizeSubstat
