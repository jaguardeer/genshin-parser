import sys
import cv2 as cv
import pytesseract
from common import *
import os

### RECTS FOR ROIS
iconRect = (1595, 205, 137, 135)
nameRect = (1375, 136, 361, 40)
levelRect = (1376, 390, 44, 22)
mainstatRect = (1376, 253, 199, 30)
#substats
left, top = 1396, 435
width, height = 245, 21
extraSpace, heightSpacing = 3, 32
substatRects = [(left - extraSpace, top - extraSpace + offset * heightSpacing,
	width + extraSpace * 2, height + extraSpace * 2)
	for offset in range(4)
]

class textRegion:
	def __init__(self, name, rect):
		self.name = name
		self.rect = rect

	def __repr__(self):
		return f'{{name={self.name},rect={self.rect}}}'

nameRegion = textRegion('name', nameRect)
levelRegion = textRegion('level', levelRect)
mainstatRegion = textRegion('mainstat', mainstatRect)
substatRegions = [textRegion(f'substat', rect) for i, rect in enumerate(substatRects)]

textRegions = [nameRegion, levelRegion, mainstatRegion, *substatRegions]



 ### DRIVER CODE

videoFilename = sys.argv[1] if len(sys.argv) > 1 else '2023-12-09 21-52-22.mkv'
video = cv.VideoCapture(videoFilename)
if not video.isOpened():
	print('Failed to open video. Exiting...')
	exit()

class frameResult:
	pass

	def write(self):
		pass


def stripNonAlphaNum(string):
	allowedSymbol='+.%'
	return ''.join([c for c in string if c.isalnum() or c in allowedSymbol])

outDir = Path('./results')

for frameObj in iterateVideo(video):

	frameImg = frameObj['img']
	frameIndex = frameObj['index']

	for roi in textRegions:
		img = crop(frameImg, roi.rect)
		txt = stripNonAlphaNum(pytesseract.image_to_string(img).strip())
		print(f'{frameIndex}: {roi.name} = {txt}')
		filename = outDir / roi.name / txt / f'{frameIndex}.png'
		try:
			os.makedirs(filename.parent, exist_ok = True)
			write_success = cv.imwrite(str(filename), img)
		except:
			write_success = False
		if not write_success:
			f = open('results/failed_writes.txt', mode='a')
			f.write(f'{filename}\n')
			f.close()