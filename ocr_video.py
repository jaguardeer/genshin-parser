import cv2 as cv
import pytesseract
import numpy as np
import validate_ocr
from util import *

## todo:
## other fields (mainStatKey, level, slot, set)
## set might be easier by item name?
## cv pyramids?
## generate images here instead of template dir
## log stuff:
## -- log images
## -- errors
## -- corrections
## -- dupes

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
	frameCount = 0
	while video.read(frameBuffer)[0]:
		frameCount += 1
		substatRegion = frameBuffer[473:632, 1357:1665]
		#diff = np.sum(cv.erode(np.abs(substatRegion - prevFrame), np.ones((2, 2), np.uint8)))
		diffImg = cv.cvtColor(substatRegion - prevFrame, cv.COLOR_BGR2GRAY)
		thresh = 8
		_, diffImg = cv.threshold(diffImg, thresh, None, cv.THRESH_TOZERO)
		_, diffImg = cv.threshold(diffImg, 255 - thresh, None, cv.THRESH_TOZERO_INV)
		diff = cv.countNonZero(cv.erode(diffImg, np.ones((2, 2), np.uint8)))
		#print(f"{frameCount}: {diff}")
		if diff > 9_000:
			#print(f"frame {frameCount} diff {diff}")
			#cv.imwrite(f"./frames2/{str(frameCount)}.png", frameBuffer)
			yield cv.cvtColor(frameBuffer, cv.COLOR_BGR2GRAY), frameCount
		np.copyto(prevFrame, substatRegion)

def parseVideo(video, regions):
	results = list(map(lambda f: parseFrame(f, regions), iterateVideo(video, regions)))
	return results
	#valid = validate_ocr.validateResult(r)

def sliceRegion(vidFrame, region):
	return vidFrame[*[slice(*x) for x in region]]

def parseFrame(frameInfo, regions):
	vidFrame, frameNum = frameInfo
	regionImages = map(lambda r: sliceRegion(vidFrame, r), regions.values())
	frameResult = map(parseImg, regionImages, regions.keys())
	finalResult = dict(frameResult)
	finalResult["frameNumber"] = frameNum
	#print(finalResult)
	return finalResult

## process image for template matching
def processImage(img):
	## binarize and crop to bounding box
	_, binImg = cv.threshold(img, 128 ,255, cv.THRESH_BINARY_INV)
	binRect = cv.boundingRect(binImg)
	finalImg = crop(img, binRect)
	return finalImg

## new parsing using simple image matching
from template_match import *
templateDir = "./templates"
templateFiles = os.listdir(templateDir)
templateImages = [(file, cv.imread(f"{templateDir}/{file}", 0)) for file in templateFiles]
worstAbs = 100_000_000
worstRel = 0
## todo: return confidence = 1 - best / second best
def parseImg(img, regionKey):
	binImg = processImage(img)
	if(binImg.shape[0] * binImg.shape[1] < 100): return regionKey, ("", -1)
	def calcDiff(templateImg):
		diff = getMatchCoeff(binImg, templateImg)
		#print(f"diff is {round(diff, 3)} for {file}")
		return diff
	results = list(map(lambda x: {"fn": x[0], "score": calcDiff(x[1])}, templateImages))
	results.sort(key = lambda x: x["score"])
	best = results[0]
	secondBest = results[1]
	#print(best, secondBest)
	#if secondBest["score"] - best["score"] < 100:
		#print(best, secondBest)
	confRel = best['score'] / secondBest['score']
	confAbs = secondBest['score'] - best['score']
	global worstAbs
	global worstRel
	if(confAbs < worstAbs):
		print(f'new worst: {confAbs} for {best["fn"]} vs {secondBest["fn"]}, rel was {confRel}')
		worstAbs = confAbs
		#cv.imshow(results[0]['fn'], img)
		cv.imwrite(f'./worst/{results[0]["fn"]}', img)
		cv.waitKey()
		cv.destroyAllWindows()
	if(confRel > worstRel):
		print(f'new worst: {confRel} for {best["fn"]} vs {secondBest["fn"]}, abs was {confAbs}')
		worstRel = confRel
		#cv.imshow(results[0]['fn'], img)
		cv.imwrite(f'./worst/{results[0]["fn"]}', img)
		cv.waitKey()
		cv.destroyAllWindows()
	textRaw = results[0]["fn"].rstrip(".png")
	return regionKey, (textRaw, int(best["score"]))#, confRel, confAbs

def main():
	start = time.time()
	#videoPath = "./stream.mkv"
	videoPath = './stream.mkv'
	regionsPath = "./regions.json"

	video = cv.VideoCapture(videoPath)
	regions = loadJsonFile(regionsPath)

	results = parseVideo(video, regions)
	outFile = open("artifacts.json", "w")
	json.dump(results, outFile, indent = 2, skipkeys = True)
	outFile.close()
	print(f"took {time.time() - start} seconds")

## Only run main if not in -i and not imported
import sys
if sys.flags.interactive == 0 and __name__ == "__main__" : main()
