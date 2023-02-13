import cv2 as cv
import numpy as np
import pytesseract
from common import *

# TODO: skip Sanctifying Essence & the other one
# TODO: binarize by distance from font color?
# TODO: change frame culling, look at more than substat area
# TODO: save cache to disk
# TODO: write caching functions (as object?)
## if generating my own templates
## 20pt font for substats
## 18pt for mainstatkey

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
		#parseIcon,		# -> setKey, slotKey
		parseIcon,		# -> name TODO: just do name -> name?
		parseLevel,		# -> level
		parseRarity,	# -> rarity
		parseMainStat,	# -> mainStatKey
		parseLocation,	# -> location
		parseLock,		# -> lock
		parseSubstats	# -> substats[]
	]
	parseResults = {key: val for parse in parseFuncs for key, val in parse(frame).items()}
	return parseResults


###### ICON, LEVEL, MAINSTAT PARSING

## takes frame, returns name
def parseIcon(frame):
	iconRegion = (1585, 205, 137, 135)
	#nameRegion = (1364, 133, 365, 44)
	nameRegion = (1365, 136, 361, 40)
	iconImg = crop(frame, iconRegion)
	global iconImgCache
	cacheMatches = (x for x in iconImgCache if isSameImg(iconImg, x['img']))
	cacheResult = next(cacheMatches, None)
	if not cacheResult:
		nameImg = crop(frame, nameRegion)
		nameImg = cv.copyMakeBorder(nameImg, 5, 5, 5, 5, cv.BORDER_CONSTANT, value = nameImg[-1, -1].tolist())
		strResult = imageToString(nameImg)
		#print(strResult)
		#cv.imshow('test', nameImg)
		#cv.waitKey(1)
		iconImgCache.append({'strResult': strResult, 'img': np.copy(iconImg)})
	else:
		strResult = cacheResult['strResult']
	## (optional) Check if extra matches just to be safe
	for extraMatch in []:#cacheMatches:
		diff = calcImageDiff(iconImg, extraMatch['img'])
		print(f'extra match for {strResult}, diff was {diff}')
		print(len(iconImgCache))
	return {'name': strResult}

## tesseract was having trouble with the level img crop. this func adds extra margins
def levelImgToString(img):
	img = cv.copyMakeBorder(img, 3, 3, 3, 3, cv.BORDER_REPLICATE)
	strResult = imageToString(img)
	return strResult

## parseLevel takes whole frame, returns {level}
def parseLevel(frame):
	levelRegion = (1368, 390, 44, 22)
	img = crop(frame, levelRegion)
	## Check cache, parse and add new entry if no match
	global levelImgCache
	cacheMatches = (x for x in levelImgCache if isSameImg(img, x['img']))
	cacheResult = next(cacheMatches, None)
	if not cacheResult:
		strResult = levelImgToString(img)
		levelImgCache.append({'strResult': strResult, 'img': np.copy(img)})
	else:
		strResult = cacheResult['strResult']
	## (optional) Check if extra matches just to be safe
	for extraMatch in []:#cacheMatches:
		diff = calcImageDiff(img, extraMatch['img'])
		print(f'extra match for {strResult}, diff was {diff}')
		print(len(levelImgCache))
	return {'level': strResult}

def isSameMainstatImg(imgA, imgB):
	## take absolute diff and threshold
	thresh = 10
	diffImg = cv.absdiff(imgA, imgB)
	_, binImg = cv.threshold(diffImg, thresh, 255, cv.THRESH_BINARY)
	## convert to grayscale (todo)
	binImg = cv.cvtColor(binImg, cv.COLOR_BGR2GRAY)
	## postprocess diff img - remove lonely pixels
	kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
	erodeImg = cv.morphologyEx(binImg, cv.MORPH_OPEN, kernel, iterations = 1)
	## count remaining pixels
	diff = cv.countNonZero(erodeImg)
	return diff < 10


## img of mainstat -> string (todo: take rarity as arg? for known bgcolor)
def mainStatImgToString(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	#img = cv.dilate(img, np.ones((2, 2), np.uint8))
	#cv.imshow('b', img)
	#cv.waitKey()
	#_, img = cv.threshold(img, 140, 255, cv.THRESH_BINARY)
	#img = cv.medianBlur(img, 3)
	txt = pytesseract.image_to_string(img)
	#cv.imshow('a', img)
	return txt.strip()


## takes frame, returns {mainStatKey}
def parseMainStat(frame):
	#mainStatRegion = (1360, 257, 199, 26)
	mainStatRegion = (1366, 253, 199, 30)
	img = crop(frame, mainStatRegion)
	#img = cv.medianBlur(img, 3)
	img = cv.dilate(img, np.ones((2, 2), np.uint8))
	## Check cache, parse and add new entry if no match
	global mainStatImgCache
	cacheMatches = (x for x in mainStatImgCache if isSameMainstatImg(img, x['img']))
	cacheResult = next(cacheMatches, None)
	if not cacheResult:
		strResult = mainStatImgToString(img)
		mainStatImgCache.append({'strResult': strResult, 'img': np.copy(img)}) ## does img need copy?
	else:
		strResult = cacheResult['strResult']
	## (optional) Check if extra matches just to be safe
	for extraMatch in []:#cacheMatches:
		print(f'extra match for {strResult}')
		cv.imshow('orig', img)
		cv.imshow('cached', extraMatch['img'])
		cv.waitKey()
	return {'mainStatKey': strResult}


###### NOT IMPLEMENTED YET

## takes frame, returns {location}
def parseLocation(frame):
	return {'location': ''}

## takes frame, returns {lock}
def parseLock(frame):
	return {'lock': False}



###### RARITY PARSING


## takes frame, returns {rarity}
def parseRarity(frame):
	cols = [1377, 1405, 1433, 1462, 1489]
	row = 342
	numLines = next((i for i, x in enumerate(cols) if frame[row, x, 1] < 170), len(cols))
	return {'rarity': numLines}


###### SUBSTAT PARSING

## takes frame, returns # of substat lines
def countSubstatLines(frame):
	col = 1376
	rows = range(443, 540, 32)
	numLines = next((i for i, x in enumerate(rows) if frame[x, col, 1] >= 128), len(rows))
	return numLines

## takes frame, returns {substats[]}
def parseSubstats(frame):
	numSubstatLines = countSubstatLines(frame)
	## these values found through experimentation
	left, top = 1386, 435
	width, height = 245, 21
	extraSpace, heightSpacing = 3, 32
	substatRegions = [(left - extraSpace, top - extraSpace + offset * heightSpacing,
		width + extraSpace * 2, height + extraSpace * 2)
		for offset in range(numSubstatLines)
	]
	results = [parseSubstatImg(crop(frame, region)) for region in substatRegions]
	return {'substats': results}

## parseSubstatImg takes img of just the substat line, returns string
## substatImgCache is list of (img, strResult) pairs for previously OCR'd images
def parseSubstatImg(img):
	## Check cache, parse and add new entry if no match
	global substatImgCache
	cacheMatches = (x for x in substatImgCache if isSameImg(img, x['img']))
	cacheResult = next(cacheMatches, None)
	if not cacheResult:
		strResult = imageToString(img)
		substatImgCache.append({'strResult': strResult, 'img': np.copy(img)})
	else:
		strResult = cacheResult['strResult']
	## (optional) Check if extra matches just to be safe
	for extraMatch in []:#cacheMatches:
		print(f'extra match for {strResult}')
		cv.imshow('extra', extraMatch['img'])
		cv.imshow('orig', img)
		cv.waitKey()
	return strResult



######  IMAGE PROCESSING / MATCHING FUNCS
## todo: proper cache

def imageToString(img):
	strResult = pytesseract.image_to_string(img)
	return strResult.strip()

def calcImageDiff(imgA, imgB):
	## take absolute diff and threshold
	thresh = 52
	diffImg = cv.absdiff(imgA, imgB)
	_, binImg = cv.threshold(diffImg, thresh, 255, cv.THRESH_BINARY)
	## convert to grayscale (todo)
	binImg = cv.cvtColor(binImg, cv.COLOR_BGR2GRAY)
	## postprocess diff img - remove lonely pixels
	kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
	erodeImg = cv.morphologyEx(binImg, cv.MORPH_OPEN, kernel, iterations = 1)
	## count remaining pixels
	diff = cv.countNonZero(erodeImg)
	return diff


def isSameImg(imgA, imgB):
	a = imgA
	b = imgB
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
	return len([x for x in rows if frame[x, col, 1] < 128])



###### IMAGE CACHING
## TODO: make this not be global state
mainStatImgCache = []
levelImgCache = []
substatImgCache = []
iconImgCache = []

def loadImgCache(cacheJsonFilename):
	cacheData = loadJsonFile(cacheJsonFilename)
	imgCache = [{
		'strResult': x['strResult'],
		'img': cv.imread(x['imgFilename'])
		} for x in cacheData]

def loadImgCaches():


def writeImgCache(imgCache):
	outData = [{'strResult': x['strResult'], 'imgFilename': cacheDir}]


######  DRIVER CODE

if __name__ == '__main__':
	import json
	import sys
	from pathlib import Path

	## parse args
	videoFilename = sys.argv[1] if len(sys.argv) > 1 else '2023-01-15 17-48-41.mp4'
	video = cv.VideoCapture(videoFilename)
	#print(videoFilename)

	vidParseResults = [parseFrame(frameObj['img']) | {'frameIndex': frameObj['index']} for frameObj in iterateVideo(video, frameSkipTest = frameSkipTest)]

	## todo: deduplicate (frameIndex makes same artis look unique)
	goodFormatArtifacts = [cvtGOOD(x) for x in vidParseResults]
	outData = {
		'format': 'GOOD',
		'source': Path(__file__).stem,
		'version':1,
		'artifacts': goodFormatArtifacts
	}
	outFilename = getResultsFilename(videoFilename, __file__)
	outFile = open(outFilename, 'w')
	json.dump(outData, outFile)
	outFile.close()
	k = goodFormatArtifacts[0].keys()
	print([x for x in goodFormatArtifacts for i in k if x[i] == 'invalid'])



## TODO: how many frames skipped / processed?
## generate text?

## (longterm) frame detector -> do different stuff per frame (looking at inv, upgrading artis, w/e)

## for each text result:
## how many buckets produced that result? (ideally 1)