import cv2 as cv
import numpy as np
import time
from util import *
import os

def getMatchCoeff(img, template):
	## resize to match template size
	h, w, *channels = template.shape
	resized = cv.resize(img, (w, h))
	## todo: learn what different matching methods do
	matchImg = cv.matchTemplate(resized, template, cv.TM_CCOEFF_NORMED)
	## best fit matching
	minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(matchImg)
	return maxVal, maxLoc

def main():
	sourceImg = cv.imread('artifact-page.png')
	templateDir = "./templates"
	templateFiles = os.listdir(templateDir)

	## select ROI
	roi = cv.selectROI(sourceImg)
	cropImg = crop(sourceImg, roi)

	## binarize and crop to bounding box
	grayImg = cv.cvtColor(cropImg, cv.COLOR_BGR2GRAY)
	_, binImg = cv.threshold(grayImg, 128 ,255, cv.THRESH_BINARY_INV)
	binRect = cv.boundingRect(binImg)
	binImg = crop(binImg, binRect)

	start = time.time()
	for file in templateFiles:
		template = cv.imread(f"{templateDir}/{file}", 0)

		## run template matching
		maxVal, maxLoc = getMatchCoeff(binImg, template)
		print(f"match coeff is {round(maxVal, 3)} for {file} at {maxLoc}")

		## draw rect around matched point
		pt = (maxLoc[0] + roi[0], maxLoc[1] + roi[1])
		w, h = binRect[2] - binRect[0], binRect[3] - binRect[1]
		cv.rectangle(sourceImg, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)

		## show, write results
		#show(sourceImg)
	print(f"took {time.time() - start} seconds")

if __name__ == "__main__": main()
