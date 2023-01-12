import cv2 as cv
import pytesseract
import numpy as np
import validate_ocr
from util import *

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



def getVideoShape(video):
	width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
	return height, width, 3

def checkFrameDiff():
	return None

## frame skipping logic goes in here
## look at substat area only
from template_match import getMatchCoeff
def iterateVideo(video, regions):
	prevFrame = np.ones((159, 308, 3), np.uint8)
	frameBuffer = np.empty(getVideoShape(video), np.uint8)
	i = 0
	while video.read(frameBuffer)[0]:
		i += 1
		substatRegion = frameBuffer[473:632, 1357:1665]
		diff = np.sum(cv.erode(np.abs(substatRegion - prevFrame), np.ones((2, 2), np.uint8)))
		#print(f"{i}: {diff}")
		if diff > 1_500_000:
			#print(f"frame {i}")
			cv.imwrite(f"./frames2/{str(i)}.png", frameBuffer)
			yield cv.cvtColor(frameBuffer, cv.COLOR_RGB2GRAY)
		np.copyto(prevFrame, substatRegion)

def parseVideo(video, regions):
	results = list(map(lambda f: parseFrame(f, regions), iterateVideo(video, regions)))
	return results
	#valid = validate_ocr.validateResult(r)

def sliceRegion(vidFrame, region):
	return vidFrame[*[slice(*x) for x in region]]

def parseFrame(vidFrame, regions):
	regionImages = map(lambda r: sliceRegion(vidFrame, r), regions.values())
	frameResult = map(parseImg, regionImages, regions.keys())
	return dict(frameResult)

## process image for template matching
def processImage(img):
	## binarize and crop to bounding box
	_, binImg = cv.threshold(img, 128 ,255, cv.THRESH_BINARY_INV)
	binRect = cv.boundingRect(binImg)
	binImg = crop(binImg, binRect)
	return binImg

## new parsing using simple image matching
from template_match import *
templateDir = "./templates"
templateFiles = os.listdir(templateDir)
warnCount = 0

def parseImg(img, regionKey):
	binImg = processImage(img)
	if(binImg.shape[0] * binImg.shape[1] < 100): return regionKey, ("", -1)
	def calcDiff(file):
		template = cv.imread(f"{templateDir}/{file}", 0)
		diff = getMatchCoeff(binImg, template)
		#print(f"diff is {round(diff, 3)} for {file}")
		return diff
	results = list(map(lambda x: {"fn": x, "score": calcDiff(x)}, templateFiles))
	results.sort(key = lambda x: x["score"])
	best = results[0]
	secondBest = results[1]
	#print(best, secondBest)
	if best["score"] > 10:
		print(best, secondBest)
		global warnCount
		warnCount += 1
	textRaw = results[0]["fn"].rstrip(".png")
	return regionKey, (textRaw, int(best["score"]))

def main():
	start = time.time()
	videoPath = "./stream.mkv"
	regionsPath = "./regions.json"

	video = cv.VideoCapture(videoPath)
	regions = loadJsonFile(regionsPath)

	results = parseVideo(video, regions)
	outFile = open("artifacts.json", "w")
	json.dump(results, outFile, skipkeys = True)
	outFile.close()
	global warnCount
	print(warnCount)
	print(f"took {time.time() - start} seconds")

## Only run main if not in -i and not imported
import sys
if sys.flags.interactive == 0 and __name__ == "__main__" : main()
