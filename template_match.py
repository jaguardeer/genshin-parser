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

def main():
	sourceImg = cv.imread('artifact-page2.png')
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
	def calcDiff(file):
		template = cv.imread(f"{templateDir}/{file}", 0)
		diff = getMatchCoeff(binImg, template)
		#print(f"diff is {round(diff, 3)} for {file}")
		return diff

	results = list(map(lambda x: {"fn": x, "score": calcDiff(x)}, templateFiles))
	
	print(f"ran {len(results)} checks in {round(time.time()-start, 3)*1000}ms")
	results.sort(key = lambda x: x["score"])
	from pprint import pprint
	pprint(results[0:20])
	return results

if __name__ == "__main__": main()
