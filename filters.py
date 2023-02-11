
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


sampleFiles = [
	'./sift/mainstat/Anemo DMG Bonus/2023-01-15 17-48-41.mp4.468.png',
	'./sift/substats/ATK+3.7_/2023-01-15 17-48-41.mp4.5520.png',
	'./sift/mainstat/HP/2023-01-15 17-48-41.mp4.1154.png'
]

sampleImages = [cv.imread(f) for f in sampleFiles]



def identity(img):
	return img

def greyscale(img):
	return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def dilated(img):
	return cv.dilate(img, np.ones((3, 3), np.uint8))

def sobel(img):
	img = greyscale(img)
	img = cv.Sobel(img, -1, 1, 1)
	return img

def hsv0(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2HLS)
	img = img[:, :, 0]
	return img

def hsv1(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2HLS)
	img = img[:, :, 1]
	return img

def hsv2(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2HLS)
	img = img[:, :, 2]
	return img

def grayThenThresh(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	_, img = cv.threshold(img, 128, 255, cv.THRESH_BINARY)
	return img

def grayThenThreshINV(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	_, img = cv.threshold(img, 128, 255, cv.THRESH_BINARY_INV)
	return img


filterFuncs = [
	identity, hsv0, hsv1, hsv2
]


def plotWithFilter(plot, img, func):
	## run filter
	img = func(img)
	## handle color
	isGray = img.ndim == 2
	cmap = 'gray' if isGray else None
	if not isGray:
		img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	## plot the img
	title = func.__name__
	plot.imshow(img, cmap = cmap)
	plot.axis('off')
	plot.set_title(title)


numSamples = len(sampleImages)
numFilters = len(filterFuncs)
fig, subplots = plt.subplots(numSamples, numFilters)

#subplots[0][0].imshow(filteredImages[0][0])

#for y, img in enumerate(sampleImages):
#	subplots[y][0].imshow(img)

for plotRow, img in zip(subplots, sampleImages):
	for plot, func in zip(plotRow, filterFuncs):
		plotWithFilter(plot, img, func)


fig.tight_layout()
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()