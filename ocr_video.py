import cv2 as cv
import pytesseract
import numpy as np
import json
import validate_ocr

## todo:
## cv pyramids
## use tesseract dll?
## log stuff:
## -- errors
## -- corrections
## -- dupes
## add more/better corrections (stat names)
## if I still save images to disk, use my own wrapper for tesseract

## for debug
def moveWindows():
	positions = {
		"name": (1000, 500),
		"level": (1000, 600),
		"mainstat_name": (1450, 500),
		"slot": (1150, 600),
		"substats": (1000, 700),
		"sub1": (1400, 600),
		"sub2": (1400, 700),
		"sub3": (1400, 800),
		"sub4": (1400, 900)
	}
	for name in positions:
		cv.moveWindow(name,*positions[name])

## TODO: move this to util
def loadJsonFile(filename):
	f = open(filename)
	obj = json.load(f)
	f.close()
	return obj

def getVideoShape(video):
	width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
	return height, width, 3

## frame skipping logic goes in here
## look at substat area only
def iterateVideo(video, regions):
	frameBuffer = np.empty(getVideoShape(video), np.uint8)
	while video.read(frameBuffer)[0]:
		yield cv.cvtColor(frameBuffer, cv.COLOR_RGB2GRAY)

def parseVideo(video, regions):
	results = map(lambda f: parseFrame(f, regions), iterateVideo(video, regions))
	for r in results:
		print(r)
		validate_ocr.validateResult(r)

def sliceRegion(vidFrame, region):
	return vidFrame[*[slice(*x) for x in region]]

## process image for OCR. standard erode/dilate/binarize/scale
def processImage(img):
	erodeKernel = np.ones((2, 2), np.uint8)
	dilateKernel = np.ones((2, 2), np.uint8)
	imgResult = cv.erode(img, erodeKernel)
	imgResult = cv.dilate(imgResult, dilateKernel)
	_, imgResult = cv.threshold(imgResult, 128 ,255, cv.THRESH_BINARY | cv.THRESH_OTSU)
	imgResult = cv.resize(imgResult, None, fx=8, fy=8, interpolation=cv.INTER_CUBIC)
	return imgResult

def parseFrame(vidFrame, regions):
	regionImages = map(lambda r: sliceRegion(vidFrame, r), regions.values())
	results = map(parseImg, regionImages, regions.keys())
	return dict(results)

def parseImg(img, key):
	imgProcessed = processImage(img)
	textRaw = pytesseract.image_to_string(imgProcessed) # todo - configs?
	return key, textRaw

def main():
	videoPath = "./stream.mkv"
	regionsPath = "./regions.json"

	video = cv.VideoCapture(videoPath)
	regions = loadJsonFile(regionsPath)

	parseVideo(video, regions)

## Only run main if not in -i and not imported
import sys
if sys.flags.interactive == 0 and __name__ == "__main__" : main()