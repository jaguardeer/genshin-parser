import cv2 as cv
import numpy as np
import json


###### VIDEO AND IMG FUNCS
def crop(img, region):
	return img[region[1]:region[1]+region[3], region[0]:region[0]+region[2]]


## TODO: proper channels
def getVideoShape(video):
	width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
	return height, width, 3

## frameSkipTest(curr, prev) -> return True if frame should be skipped
## todo: frameSkipTest(frame) and then use static local prev in func?
## todo: preallocating buffer breaks stuff, loss of precision?
def iterateVideo(video, frameSkipTest = lambda curr, prev: False):
	frameIndex = 0
	currBuffer = np.empty(getVideoShape(video), np.uint8)
	prevBuffer = np.zeros(getVideoShape(video), np.uint8)
	while True:
		success, _ = video.read(currBuffer)
		#success, curFrame = video.read()
		if not success: break
		#if frameIndex == 0 or not frameSkipTest(curFrame, prevFrame):
		if frameIndex == 0 or not frameSkipTest(currBuffer, prevBuffer):
			yield {'index': frameIndex, 'img': currBuffer}
		frameIndex += 1
		currBuffer, prevBuffer = prevBuffer, currBuffer
		#prevFrame = curFrame


def getFrame(video, frameIndex):
	video.set(cv.CAP_PROP_POS_FRAMES, frameIndex)
	success, img = video.read()
	return img if success else None

def viewFrame(video, frameIndex):
	img = getFrame(video, frameIndex)
	cv.imshow(str(frameIndex), img)
	cv.waitKey()


###### FILE IO

def loadJsonFile(filename):
	f = open(filename)
	obj = json.load(f)
	f.close()
	return obj

from pathlib import Path
def getResultsFilename(vidFilename, scriptName):
	vidStem = Path(vidFilename).stem
	scriptStem = Path(scriptName).stem
	suffix = 'json'
	outFile = '.'.join([vidStem, scriptStem, suffix])
	return outFile




###### OCR STRING VALIDATION
import re
from strKeyDicts import *

## check that substat string (ex: "ATK+4.1%") matches KEY+VALUE format
## todo: tesseract sometimes adds extra whitespace but idc (always 'Elemental Mastery+17'? probably)
def isValidSubstatString(substatString):
	keyPattern = '(?:' + '|'.join(SUBSTAT_KEY_STRINGS.keys()) + ')'
	pattern = keyPattern + '\\+(?:[0-9],)?[0-9]+(?:\\.[0-9]%)?'
	return None != re.fullmatch(pattern, substatString)


## todo - doesn't actually check range yet
def isValidLevelString(levelString):
	pattern = '\\+[0-9]'
	return None != re.fullmatch(pattern, levelString)




###### GOOD FORMAT CONVERTION
## GOOD format wants:
## -- setKey
## -- rarity
## -- level
## -- mainStatKey
## -- substats
## -- optional: location, exclude, lock, id
## genshin optimizer will accept invalid artifacts (wrong substats f. ex)
## artifact entries can have extra keys

def raw2goodMainstat(rawStr, slotKey):
	## check if valid key
	if rawStr not in MAINSTAT_KEY_STRINGS.keys():
		return 'invalid'
	## all mainstats except flower / plume are %, so they end with '_'
	statKey = MAINSTAT_KEY_STRINGS[rawStr]
	flatSlot = ['flower', 'plume']
	flatStat = ['eleMas']
	suffix = '' if slotKey in flatSlot or statKey in flatStat else '_'
	return statKey + suffix

## todo: error checking / validation?
def raw2goodSubstat(rawStr):
	try:
		namePart, valPart = rawStr.split("+")
		key = SUBSTAT_KEY_STRINGS[namePart] + ("_" if valPart.endswith("%") else "")
		val = float(valPart.rstrip("%").replace(',', ''))
		return {'key': key, 'value': val}
	except ValueError:
		return {'key': 'invalid', 'value': -1}

def stripNonAlpha(string):
	return ''.join([c for c in string if c.isalpha()])
	
def to_pascal(name):
	return ''.join(c for c in ''.join(word.capitalize()
		for word in name.split(' '))
		if c.isalnum())

def rawName2SetSlot(rawName):
	# To derive the PascalKey from a specific name, remove all symbols from the name, and Capitalize each word:
	rawName = stripNonAlpha(rawName)
	return NAME_SET_SLOT_KEY_STRINGS.get(rawName, {'setKey': 'invalid', 'slotKey': 'invalid'})

def cvtSubstats(substats):
	return [raw2goodSubstat(x) for x in substats]

def raw2goodLevel(rawStr):
	try:
		return int(rawStr.lstrip('+'))
	except ValueError:
		return -1

def cvtGOOD(rawArtifact):
	cvtFuncs = {
		'level': raw2goodLevel,
		'substats': cvtSubstats,
	}
	goodArtifact = {key: cvtFuncs.get(key, lambda x: x)(val) for key, val in rawArtifact.items()}
	setKey, slotKey = rawName2SetSlot(rawArtifact['name']).values()
	goodArtifact['setKey'] = setKey
	goodArtifact['slotKey'] = slotKey
	goodArtifact['mainStatKey'] = raw2goodMainstat(rawArtifact['mainStatKey'], slotKey)
	return goodArtifact






