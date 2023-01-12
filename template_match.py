import cv2 as cv
import numpy as np
import time
from util import *

def getMatchCoeff(img, template):
	## resize to match template size
	h, w, *channels = template.shape
	resized = cv.resize(img, (w, h))
	## todo: learn what different matching methods do
	matchImg = cv.matchTemplate(resized, template, cv.TM_CCOEFF_NORMED)
	## best fit matching
	minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(matchImg)
	print(f"match coeff is {round(maxVal, 3)}")
	return maxVal, maxLoc

def main():
	sourceImg = cv.imread('artifact-page.png')
	template = cv.imread('test-template.png', 0)

	## select ROI
	roi = cv.selectROI(sourceImg)
	cropImg = crop(sourceImg, roi)

	## binarize and crop to bounding box
	grayImg = cv.cvtColor(cropImg, cv.COLOR_BGR2GRAY)
	_, binImg = cv.threshold(grayImg, 128 ,255, cv.THRESH_BINARY_INV)
	binRect = cv.boundingRect(binImg)
	binImg = crop(binImg, binRect)

	## run template matching
	maxVal, maxLoc = getMatchCoeff(binImg, template)

	## draw rect around matched point
	pt = (maxLoc[0] + roi[0], maxLoc[1] + roi[1])
	w, h = binRect[2] - binRect[0], binRect[3] - binRect[1]
	cv.rectangle(sourceImg, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)

	## show, write results
	show(sourceImg)
	cv.imwrite('res.png', cropImg)

if __name__ == "__main__": main()
