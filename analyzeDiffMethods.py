from common import *


## erode to kill stray jpeg'd pixels that pass thresh?
def simpleCrop(img):
	## black on white
	size = (3, 3)
	#img = cv.medianBlur(img, size)
	grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	grayImg = cv.GaussianBlur(grayImg,size,0)
	_, binImg = cv.threshold(grayImg, 128, 255, cv.THRESH_BINARY_INV)
	box = cv.boundingRect(binImg)
	newImg = crop(img, box)
	if newImg.shape != img.shape:
		return crop(img, box)
	else:
		grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
		grayImg = cv.GaussianBlur(grayImg,size,0)
		_, binImg = cv.threshold(grayImg, 136, 255, cv.THRESH_BINARY)
		box = cv.boundingRect(binImg)
		newImg = crop(img, box)
		if newImg.shape != img.shape:
			return crop(img, box)
	print('u made a bad assumption')
	return None


def simpleDiff(imgA, imgB):
	imgs = [imgA, imgB]
	imgA, imgB = [simpleCrop(img) for img in imgs]
	h, w, *channels = imgB.shape
	imgA = cv.resize(imgA, (w, h), interpolation = cv.INTER_LINEAR)
	diff = cv.absdiff(imgA, imgB)
	return np.sum(diff)


def calcVariance(imageList, diffMethod):
	return [diffMethod(a, b) for a in imageList for b in imageList]


if __name__ == '__main__':
	import os
	from pprint import pprint

	#parentDir = './sift/substats'
	#folders = os.listdir(parentDir)

	parentDir = './sift'
	folders = [f'{child}/{f}' for child in os.listdir(parentDir) for f in os.listdir(f'{parentDir}/{child}')]
	#pprint(folders)

	folderLens = [len(os.listdir(f'{parentDir}/{f}')) for f in folders]

	#tf = './sift/substats/Energy Recharge+5.8_'

	minHeights = {}
	maxHeights = {}
	minWidths = {}
	maxWidths = {}
	shapeNames = {}
	for folder in folders:
		tf = f'{parentDir}/{folder}'
		files = os.listdir(tf)
		images = [cv.imread(f'{tf}/{file}') for file in files]
		crops = [simpleCrop(i) for i in images]
		shapes = [i.shape for i in crops]
		shapeNames[folder] = list(zip(files, shapes))
		minHeights[folder] =  min(s[0] for s in shapes)
		maxHeights[folder] =  max(s[0] for s in shapes)
		minWidths[folder] =  min(s[1] for s in shapes)
		maxWidths[folder] =  max(s[1] for s in shapes)
	pprint('HEIGHTS')
	pprint([(k, minHeights[k], maxHeights[k]) for k in minHeights if minHeights[k] != maxHeights[k]])
	pprint(f'max diff: {max([maxh - minh for maxh, minh in zip(maxHeights.values(), minHeights.values())])}')
	pprint('WIDTHS')
	pprint([(k, minWidths[k], maxWidths[k]) for k in minWidths if minWidths[k] != maxWidths[k]])
	maxdiff = max([maxw - minw for maxw, minw in zip(maxWidths.values(), minWidths.values())])
	pprint(f'max diff: {maxdiff}')
	pprint([k for k in maxWidths if maxWidths[k] - minWidths[k] == maxdiff])

	#variance = calcVariance(images, simpleDiff)
	#pprint(variance)
	#print

	#for i in images:
	#	cv.imshow('test', simpleCrop(i))
	#	cv.waitKey(1)

	#folderInfos = list(zip(folders, folderLens))
	#folderInfos.sort(key = lambda i: i[1])
	#pprint(folderInfos)