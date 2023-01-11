import cv2 as cv
import numpy as np
import time
from util import *

sourceImg = cv.imread('artifact-page.png')
grayImg = cv.cvtColor(sourceImg, cv.COLOR_BGR2GRAY)
template = cv.imread('test-template.png', 0)
#mask = cv.imread('res2.png', 0)

## select ROI
roi = cv.selectROI(sourceImg)
cropImg = crop(grayImg, roi)
_, binImg = cv.threshold(cropImg, 128 ,255, cv.THRESH_BINARY_INV)
show(binImg)

h, w, *channels = template.shape
## todo: learn what different matching methods do
matchImg = cv.matchTemplate(binImg, template, cv.TM_CCOEFF_NORMED)

"""
## multiple matching
threshold = 0.97
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
	cv.rectangle(sourceImg, pt, (pt[0] + w, pt[1] + yyh), (0,0,255), 2)
"""

## best fit matching
minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(matchImg)

pt = (maxLoc[0] + roi[0], maxLoc[1] + roi[1])
cv.rectangle(sourceImg, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)

## show, write results
show(sourceImg)
cv.imwrite('res.png', cropImg)
# print(len(list(zip(*loc[::-1]))))
