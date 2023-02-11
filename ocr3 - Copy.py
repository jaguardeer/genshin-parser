import cv2 as cv
import numpy as np
import pytesseract
from common import *

######  HIGH LEVEL LOGIC

## These are the fields needed for a GOOD formatted artifact entry
artifactEntryFields= [
	"setKey",		# setKey (see strKeyDicts.py)
	"slotKey",		# slotKey (see strKeyDicts.py)
	"level",		# level in 0-20
	"rarity",		# rarity in 1-5
	"mainStatKey",	# mainStatKey (see strKeyDicts.py)
	"location",		# Who is the artifact equipped to?
	"lock",			# Whether the artifact is locked in game.
	"substats",		# Array of {key, value} entries
]

def parseFrame(frame):
	## Each func in parseFuncs should take a whole frame and return a dict of results
	## The returned dicts will be merged and returned as the final result
	## See artifactEntryFields
	parseFuncs = [
		parseIcon,		# -> setKey, slotKey
		parseLevel,		# -> level
		parseRarity		# -> rarity
		parseMainStat,	# -> mainStatKey
		parseLocation,	# -> location
		parseLock,		# -> lock
		parseSubstats	# -> substats[]
	]
	parseResults = {key: val for parse in parseFuncs for key, val in parse(frame).items()}
	return parseResults

## takes frame, returns {setKey, slotKey}
def parseIcon(frame):
	return None

## takes frame, returns {level}
def parseLevel(frame):
	return None

## takes frame, returns {rarity}
def parseRarity(frame):
	return None

## takes frame, returns {mainStatKey}
def parseMainStat(frame):
	return None

## takes frame, returns {location}
def parseLocation(frame):
	return None

## takes frame, returns {lock}
def parseLock(frame):
	return None

## takes frame, returns {substats[]}
def parseSubstats(frame):
	numSubstatLines = countSubstatLines(frame)
	## list of rect tuples as returned by cv2.selectROI()
	substatRegions = [
		(1382, 428, 260, 30),
		(1382, 460, 260, 32),
		(1382, 491, 260, 34),
		(1383, 522, 260, 37),
	]
	results = [parseSubstatImg(crop(frame, region)) for region in substatRegions[:numSubstatLines]]
	return results


## parseSubstatImg takes img of just the substat line, returns string
## substatImgCache is list of (img, str) pairs for previously OCR'd images
substatImgCache = []
def parseSubstatImg(img):
	pImg = preprocess(img)
	cacheMatches = (b for b in substatImgCache if isSameImg(img, b['img']))


######  IMAGE CACHE FUNCS

## returns matching bucket if one is found
def checkImgBuckets(img, buckets):
	bucketMatches = (b for b in substatImgCache if isSameImg(img, b['img']))
	print(f'extra match for {index}/{imgEntry["frameIndex"]}-{imgEntry["regionKey"]} at {extraIndex}/{extraMatch[0]["frameIndex"]}-{extraMatch[0]["regionKey"]}, diff was {diff}')





######  IMAGE PROCESSING / MATCHING FUNCS
## todo: proper cache

def calcImageDiff(imgA, imgB):
	## resize to match sizes (need better method)
	if imgA.size == 0 or imgB.size == 0:
		return 0 if imgA.size == imgB.size else np.inf
	h, w, *channels = imgB.shape
	resized = cv.resize(imgA, (w, h), interpolation = cv.INTER_LINEAR)
	## take absolute diff and threshold
	thresh = 52
	diffImg = cv.absdiff(resized, imgB)
	_, binImg = cv.threshold(diffImg, thresh, 255, cv.THRESH_BINARY)
	## convert to grayscale (todo)
	binImg = cv.cvtColor(binImg, cv.COLOR_BGR2GRAY)
	## postprocess diff img - remove lonely pixels
	kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
	erodeImg = cv.morphologyEx(binImg, cv.MORPH_OPEN, kernel, iterations = 1)
	## count remaining pixels
	diff = cv.countNonZero(erodeImg)
	return diff


def preprocess(img):
	## todo: look into color quantization
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	_, binary = cv.threshold(gray, 128, 255, cv.THRESH_BINARY_INV)
	boundingRect = cv.boundingRect(binary)
	cropped = crop(img, boundingRect)
	return cropped

def isSameImg(imgA, imgB):
	a = preprocess(imgA)
	b = preprocess(imgB)
	## check if an img is empty
	if a.size == 0 or b.size == 0:
		return a.size == b.size
	diff = calcImageDiff(a, b)
	return diff < 10

def frameSkipTest(curFrame, prevFrame):
	substatRegion = (1382, 428, 260, 131)
	curr = crop(curFrame, substatRegion)
	prev = crop(prevFrame, substatRegion)
	diff = calcImageDiff(curr, prev)
	return diff == 0


## takes frame of artifact screen, returns number of substat lines
def countSubstatLines(frame):
	col = 1376
	rows = range(443, 540, 32)
	return len([x for x in rows if artifactScreen[x, col, 1] < 128])




######  DRIVER CODE

if __name__ == '__main__':
	video = cv.VideoCapture('2023-01-15 17-48-41.mp4')

	vidParseResults = [parseFrame(frameObj['img']) | {'frameIndex': frameObj['index']} for frameObj in iterateVideo(video)]




## TODO: how many frames skipped / processed?
## all regions
## generate text?

## (longterm) frame detector -> do different stuff per frame (looking at inv, upgrading artis, w/e)

## for each text result:
## how many buckets produced that result? (ideally 1)
## diff range within the result
## worst diff vs other buckets