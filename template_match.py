import cv2 as cv
import numpy as np
import time
from util import *
import os

def getMatchCoeff(img, template):
	## resize to match template size
	h, w, *channels = template.shape
	resized = cv.resize(img, (w, h), interpolation = cv.INTER_NEAREST)
	# take sum of diff
	diffImg = np.abs(template - resized)
	erodeKernel = np.ones((2, 2), np.uint8)
	diffImg = cv.erode(diffImg, erodeKernel)
	diff = np.sum(diffImg)
	#show(diffImg)
	return diff

def binarize(img):
	## binarize and crop to bounding box
	grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	_, binImg = cv.threshold(grayImg, 128 ,255, cv.THRESH_BINARY_INV)
	binRect = cv.boundingRect(binImg)
	binImg = crop(binImg, binRect)
	return binImg

import sys
def main():
	sourceFn = sys.argv[1] if len(sys.argv) > 1 else "artifact-page.png"
	sourceImg = cv.imread(sourceFn)
	templateDir = "./templates"
	templateFiles = os.listdir(templateDir)

	## select ROI
	roi = cv.selectROI(sourceImg)
	print(rect2slices(roi))
	cropImg = crop(sourceImg, roi)
	#show(cropImg)
	binimg = binarize(cropImg)

	start = time.time()
	def calcDiff(file):
		template = cv.imread(f"{templateDir}/{file}", 0)
		diff = getMatchCoeff(binImg, template)
		#print(f"diff is {round(diff, 3)} for {file}")
		return diff

	results = list(map(lambda x: {"fn": x, "score": calcDiff(x)}, templateFiles))
	
	print(f"ran {len(results)} checks in {round(time.time()-start, 3)*1000}ms")
	results.sort(key = lambda x: x["score"])
	from pprint import pprint
	pprint(results)
	return results

if __name__ == "__main__": main()
