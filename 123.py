import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

im = cv.imread('controller-view.png')
im2 = cv.imread('artifact-page.png')
assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

blurdiff = cv.medianBlur(im, 21)
edges = cv.Canny(blurdiff, 100, 120)

blurdiff = cv.medianBlur(im2, 21)
edges2 = cv.Canny(blurdiff, 100, 120)

def gallery(imgs):
	k = None
	i = 0
	while k != 27 and k != 13 and k != -1:
		cv.imshow('gallery', imgs[i % len(imgs)])
		k = cv.waitKey()
		if k == 113: i -= 1
		if k == 119: i += 1
	cv.destroyWindow('gallery')

gallery([edges, im, edges2, im2])
exit()


## driver code
def drawImg(axis, img):
	## convert color if needed
	isGray = len(img.shape) < 3
	cmap = 'gray' if isGray else None
	img = img if isGray else cv.cvtColor(img, cv.COLOR_BGR2RGB)
	axis.imshow(img, cmap = cmap)
	axis.axis('off')

## show images
numImages = len(imgs)
_, axes = plt.subplots(1, numImages)
for i in range(numImages):
	drawImg(axes[i], imgs[i])
plt.tight_layout()
figManager = plt.get_current_fig_manager()
figManager.window.state('zoomed')
plt.show()