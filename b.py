from common import getFrame, crop, viewFrame
import cv2 as cv
import pytesseract
import re
from countSubstats import countSubstatLines
from ocr3 import parseRarity



indexList = [(5970, 3), (5971, 3), (5972, 3), (5973, 3), (5974, 3), (5975, 3), (5976, 3), (6830, 3), (6831, 3), (6832, 3), (6833, 3), (6834, 3), (6835, 3), (6966, 3), (6967, 3), (6968, 3), (6969, 3), (6970, 3), (6971, 3), (6972, 3), (7339, 2), (7340, 2), (7341, 2), (7342, 2), (7343, 2), (7344, 2), (7410, 3), (7411, 3), (7412, 3), (7413, 3), (7414, 3), (7415, 3), (7416, 3), (7509, 2), (7510, 2), (7511, 2), (7512, 2), (7513, 2), (7514, 2), (7515, 2), (7594, 2), (7595, 2), (7596, 2), (7597, 2), (7598, 2), (7599, 2), (7677, 2), (7678, 2), (7679, 2), (7680, 2), (7681, 2), (7682, 2), (7683, 2), (8482, 2), (8483, 2), (8484, 2), (8485, 2), (8486, 2), (8487, 2), (8508, 2), (8509, 2), (8510, 2), (8511, 2), (8512, 2), (8513, 2), (8684, 2), (8685, 2), (8686, 2), (8687, 2), (8688, 2), (8689, 2), (8690, 2), (9311, 3), (9312, 3), (9313, 3), (9314, 3), (9315, 3), (9316, 3), (9317, 3), (9540, 2), (9541, 2), (9542, 2), (9543, 2), (9544, 2), (9545, 2), (9982, 3), (9983, 3), (9984, 3), (9985, 3), (9986, 3), (9987, 3), (9988, 3), (10105, 2), (10106, 2), (10107, 2), (10108, 2), (10109, 2), (10110, 2), (10111, 2)]

SUBSTAT_KEY_STRINGS = {
	"HP": "hp",
	"ATK": "atk",
	"DEF": "def",
	"CRIT Rate": "critRate",
	"CRIT DMG": "critDMG",
	"Energy Recharge": "enerRech",
	"Elemental Mastery": "eleMas",
}
## check that substat string (ex: "ATK+4.1%") matches KEY+VALUE format
## todo: tesseract sometimes adds extra whitespace but idc (always 'Elemental Mastery+17'?)
def isValidSubstatString(substatString):
	keyPattern = "(?:" + "|".join(SUBSTAT_KEY_STRINGS.keys()) + ")"
	pattern = keyPattern + "\\+(?:[0-9],)?[0-9]+(?:\\.[0-9]%)?"
	return None != re.fullmatch(pattern, substatString)

def checkSubstats(img, expected):
	regions = [
		{'key': 'sub1', 'rect': (1382, 428, 260, 30)},
		{'key': 'sub2', 'rect': (1382, 460, 260, 32)},
		{'key': 'sub3', 'rect': (1382, 491, 260, 34)},
		{'key': 'sub4', 'rect': (1383, 522, 260, 37)},
	]

	lines = [pytesseract.image_to_string(crop(img, r['rect'])).strip() for r in regions]
	numValid = len([l for l in lines if isValidSubstatString(l)])
	if 'Elemental Mastery +17' in lines:
		numValid += 1
	if numValid != expected:
		print(f'got {numValid}, expected {expected}')
		print('\n'.join(lines))
		#cv.imshow('b', img)
		#cv.waitKey()


if __name__ == '__main__':

	substatRegionKeys = ['sub1', 'sub2', 'sub3', 'sub4']
	video = cv.VideoCapture('2023-01-15 17-48-41.mp4')

	#viewFrame(video, 218)
	f = getFrame(video, 218)
	x = crop(f, (1360, 253, 200, 28))
	cv.imshow('x', x)
	cv.waitKey()
	#x = countSubstatLines(f)
	#y = parseRarity(f)
	#print(x, y)
	exit()

	for i, expected in indexList:
		print(i)
		frame = getFrame(video, i)
		checkSubstats(frame, expected)