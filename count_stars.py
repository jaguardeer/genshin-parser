import cv2 as cv
import numpy as np
import time
from util import *

## todo: match on binarized version
sourceImg = cv.imread('artifact-page.png')
grayImg = cv.cvtColor(sourceImg, cv.COLOR_BGR2GRAY)
template = cv.imread('test-template.png', 0)
#mask = cv.imread('res2.png', 0)

## select ROI
roi = cv.selectROI(sourceImg)
cropImg = crop(grayImg, roi)
show(cropImg)

h, w, *channels = template.shape
## todo: learn what different matching methods do
matchImg = cv.matchTemplate(cropImg, template, cv.TM_CCOEFF_NORMED)

"""
## multiple matching
threshold = 0.97
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
	cv.rectangle(sourceImg, pt, (pt[0] + w, pt[1] + yyh), (0,0,255), 2)
"""

## best fit matching
minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(matchImg)

pt = maxLoc
print(maxVal)
cv.rectangle(cropImg, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)


## show, write results
show(cropImg)
cv.imwrite('res.png', cropImg)
# print(len(list(zip(*loc[::-1]))))
