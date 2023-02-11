import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import cv2 as cv
from common import *


origImg = cv.imread('./sift/mainstat/HP/2023-01-15 17-48-41.mp4.1154.png')

#roi = cv.selectROI(origImg)
#roi = (1358, 426, 26, 166)
#roiImg = crop(origImg, roi)
roiImg = origImg



## only look at G channel
gChannel = 1
img = roiImg[:, :, gChannel]

## graph it
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(img)
ax2.hist(img)

plt.show()

## interactive stuff
winTitle = 'test'
winTitle2 = 'test2'
sliderName = 'threshold'
sliderName2 = 'threshold'

def sliderCallback(thresh):
	_, img2 = cv.threshold(img, thresh, 255, cv.THRESH_BINARY_INV)
	cv.imshow(winTitle, cv.resize(img2, None, fx = 2, fy = 2, interpolation = cv.INTER_NEAREST))

def sliderCallback2(thresh):
	_, img3 = cv.threshold(img, thresh, 255, cv.THRESH_BINARY)
	cv.imshow(winTitle2, cv.resize(img3, None, fx = 2, fy = 2, interpolation = cv.INTER_NEAREST))


cv.namedWindow(winTitle)
cv.createTrackbar(sliderName, winTitle , 255, 255, sliderCallback)
sliderCallback(255)
cv.waitKey()
cv.destroyAllWindows()
cv.namedWindow(winTitle2)
cv.createTrackbar(sliderName2, winTitle2 , 0, 255, sliderCallback2)
sliderCallback2(0)
cv.waitKey()
