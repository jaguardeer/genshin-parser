import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math



def processFullFrame(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	edges = cv.Canny(img, 100, 200, L2gradient = True)
	return edges




## load test images
testImageFiles = ['artifact-page.png', 'controller-view.png']
preImgs = [cv.imread(file) for file in testImageFiles]

## run preprocessing
postImgs = [processFullFrame(img) for img in preImgs]



## driver code
def drawImg(axis, img):
	## convert color if needed
	isGray = len(img.shape) < 3
	cmap = 'gray' if isGray else None
	img = img if isGray else cv.cvtColor(img, cv.COLOR_BGR2RGB)
	axis.imshow(img, cmap = cmap)
	axis.axis('off')

## show images
numImages = len(preImgs)
_, axes = plt.subplots(2, numImages)
for i in range(numImages):
	drawImg(axes[0][i], preImgs[i])
	drawImg(axes[1][i], postImgs[i])
plt.tight_layout()
figManager = plt.get_current_fig_manager()
figManager.window.state('zoomed')
plt.show()