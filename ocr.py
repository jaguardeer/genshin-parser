import cv2 as cv
import numpy as np
import pytesseract
from common import *
from ocr2 import *

def parseImg(img):
	return pytesseract.image_to_string(img)


regions = [
	#{'key': 'name', 'rect': (1343, 133, 408, 46), 'parseFunc': parseImg},
	#{'key': 'slot', 'rect': (1357, 182, 232, 36), 'parseFunc': parseImg},
	#{'key': 'mainstatStr', 'rect': (1356, 253, 183, 28), 'parseFunc': parseImg},
	#{'key': 'mainstatVal', 'rect': (1357, 276, 201, 49), 'parseFunc': parseImg},
	#{'key': 'rarity', 'rect': (1356, 323, 157, 36), 'parseFunc': parseImg},
	#{'key': 'level', 'rect': (1368, 390, 46, 22), 'parseFunc': parseImg},
	{'key': 'sub1', 'rect': (1382, 428, 245, 30), 'parseFunc': parseImg},
	{'key': 'sub2', 'rect': (1382, 460, 251, 32), 'parseFunc': parseImg},
	{'key': 'sub3', 'rect': (1382, 491, 260, 34), 'parseFunc': parseImg},
	{'key': 'sub4', 'rect': (1383, 522, 242, 37), 'parseFunc': parseImg},
]

def parseFrame(frame):
	frameMap = map(lambda r: {'key': r['key'], 'result': r['parseFunc'](crop(frame, r['rect']))}, regions)
	frameResults = [x for x in frameMap]
	return frameResults


if __name__ == '__main__':
	import time
	# todo: args
	video = cv.VideoCapture('2023-01-15 17-48-41.mp4')
	start = time.time()
	for frameObj in iterateVideo(video, frameSkipTest = frameSkipTest):
		frame = frameObj['img']
		index = frameObj['index']
		result = parseFrame(frame)
		print(f'{index}: {result}')
		#print(result)
		#cv.waitKey(1)
	end = time.time()
	print(f'total time was {end - start}')