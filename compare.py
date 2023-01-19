import cv2 as cv
import numpy as np
import sys
from util import *
import os

i = 0
def getMatchCoeff(img, template):
	## resize to match template size
	h, w, *channels = template.shape
	resized = cv.resize(img, (w, h), interpolation = cv.INTER_LINEAR)
	# take sum of diff (threshold both sides for uint overflow)
	diffImg = resized - template
	thresh = 32
	_, diffImg = cv.threshold(diffImg, thresh, None, cv.THRESH_TOZERO)
	_, binImg = cv.threshold(diffImg, 255 - thresh, None, cv.THRESH_TOZERO_INV)
	kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
	erodeImg = cv.morphologyEx(binImg, cv.MORPH_OPEN, kernel, iterations = 1)
	diff = cv.countNonZero(erodeImg)
	
	return diff

## process image for template matching
def processImage(img):
	## binarize and crop to bounding box
	_, binImg = cv.threshold(img, 128 ,255, cv.THRESH_BINARY_INV)
	binRect = cv.boundingRect(binImg)
	finalImg = crop(img, binRect)
	return finalImg

def compareTemplates(imageFilename, templateDir):
	templateFiles = os.listdir(templateDir)
	templates = map(lambda x: {
		'filename': x,
		'img': cv.imread(f'{templateDir}/{x}', 0)
		}, templateFiles)
	image = processImage(cv.imread(imageFilename, 0))
	results = map(lambda x: {
		'score': getMatchCoeff(image, x['img']),
		'imgFn': imageFilename,
		'templateFn': x['filename']
		}, templates)
	results = list(results)
	results.sort(key = lambda x: x['score'])
	return list(results)

worstDir = './worst'
worstFiles = [f'{worstDir}/{fn}' for fn in os.listdir(worstDir)]
from pprint import pprint

templateDir = './templates'
for worst in worstFiles:
	#print(worst)
	comparisons = compareTemplates(worst, templateDir)
	confRel = comparisons[0]['score'] / comparisons[1]['score']
	confAbs = abs(comparisons[0]['score'] - comparisons[1]['score'])
	print(f'{worst.lstrip("./worst/"):<25}{round(confRel, 3):<8}{confAbs:<8}{comparisons[0]["templateFn"]}')
	#pprint(comparisons[0:2])