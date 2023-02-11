import cv2 as cv
import numpy as np
import pytesseract
from common import *

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


if __name__ == '__main__':
	import os
	from countSubstats import countSubstatLines
	from goodConverter import *

	## init
	## regions for controller style video
	regions = [
		{'key': 'name', 'rect': (1343, 133, 408, 46)},
		#{'key': 'icon', 'rect': }
		{'key': 'slot', 'rect': (1357, 182, 232, 36)},
		{'key': 'mainstatStr', 'rect': (1356, 253, 183, 28)},
		{'key': 'mainstatVal', 'rect': (1357, 276, 201, 49)},
		{'key': 'rarity', 'rect': (1356, 323, 157, 36)},
		{'key': 'level', 'rect': (1368, 390, 46, 22)},
		{'key': 'sub1', 'rect': (1382, 428, 260, 30)},
		{'key': 'sub2', 'rect': (1382, 460, 260, 32)},
		{'key': 'sub3', 'rect': (1382, 491, 260, 34)},
		{'key': 'sub4', 'rect': (1383, 522, 260, 37)},
	]
	substatRegionKeys = ['sub1', 'sub2', 'sub3', 'sub4']
	video = cv.VideoCapture('2023-01-15 17-48-41.mp4')

	## main loop
	import time
	start = time.time()
	imgBuckets = []
	artifacts = []
	totalFrames = 0
	for frameObj in iterateVideo(video, frameSkipTest = frameSkipTest):
		totalFrames += 1
		frame = frameObj['img']
		index = frameObj['index']
		numSubstats = countSubstatLines(frame)
		arti = {}
		arti['frame'] = index
		# substats
		for k in substatRegionKeys[:numSubstats]:
			img = crop(frame, next(r['rect'] for r in regions if r['key'] == k))
			loc = {'frameIndex': index, 'regionKey': k}
			imgEntry = {'frameIndex': loc['frameIndex'], 'regionKey': loc['regionKey'], 'img': img}
			bucketMatches = ((i, b) for (i, b) in enumerate(imgBuckets) if isSameImg(img, b[0]['img']))
			index, bucket = next(bucketMatches, (None, None))
			if not bucket:
				newEntry = {'frameIndex': loc['frameIndex'], 'regionKey': loc['regionKey'], 'img': np.copy(img)}
				index = len(imgBuckets)
				imgBuckets.append([newEntry])
			for extraIndex, extraMatch in bucketMatches:
				diff = calcImageDiff(preprocess(imgEntry['img']), preprocess(extraMatch[0]['img']))
				print(f'extra match for {index}/{imgEntry["frameIndex"]}-{imgEntry["regionKey"]} at {extraIndex}/{extraMatch[0]["frameIndex"]}-{extraMatch[0]["regionKey"]}, diff was {diff}')

			## tie current artifact to the bucket
			arti[k] = index

			## (debug) save region img
			if True:
				bucketI = index if bucket else len(imgBuckets) - 1
				filename = f'./buckets/{bucketI}/{index}-{k}.png'
				dirName = os.path.dirname(filename)
				os.makedirs(dirName, exist_ok = True)
				cv.imwrite(filename, img)

		artifacts.append(arti)

	print(f'parsed {totalFrames} frames')
	print(f'grouping time was {time.time() - start}. made {len(imgBuckets)} buckets')

	tessResults = [pytesseract.image_to_string(bucket[0]['img']).strip() for bucket in imgBuckets]

	end = time.time()
	print(f'total time was {end - start}')


	SUBSTAT_KEY_STRINGS = {
		"HP": "hp",
		"ATK": "atk",
		"DEF": "def",
		"CRIT Rate": "critRate",
		"CRIT DMG": "critDMG",
		"Energy Recharge": "enerRech",
		"Elemental Mastery": "eleMas",
	}
	import re
	## check that substat string (ex: "ATK+4.1%") matches KEY+VALUE format
	def validateSubstatString(substatString):
		keyPattern = "(?:" + "|".join(SUBSTAT_KEY_STRINGS.keys()) + ")"
		pattern = keyPattern + "\\+(?:[0-9],)?[0-9]+(?:\\.[0-9]%)?"
		return None != re.fullmatch(pattern, substatString)

	artis = [[tessResults[a[k]] for k in a.keys() if k in substatRegionKeys] for a in artifacts]
	final = [[raw2goodSubstat(s) for s in a] for a in artis]

	#finalArtifacts = tessResults[x] for a[k] for k in substatRegionKeys for indexes in 
	validSubstrings = [x for x in tessResults if validateSubstatString(x)]

	import json
	validationFile = open('2023-01-15 17-48-41.json')
	validationList = json.load(validationFile)['artifacts']





## TODO: how many frames skipped / processed?
## all regions
## generate text?

## (longterm) frame detector -> do different stuff per frame (looking at inv, upgrading artis, w/e)

## for each text result:
## how many buckets produced that result? (ideally 1)
## diff range within the result
## worst diff vs other buckets