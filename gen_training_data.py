import sys
import cv2 as cv
import pytesseract
from common import *
import os

## TODO: cleanup
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

def sanitize(string):
	allowedSymbol='+.%'
	return ''.join([c for c in string if c.isalnum() or c in allowedSymbol])

def gen_training_data(videoFilename):
	out_dir = Path('./training-data')
	video = cv.VideoCapture(videoFilename)
	if not video.isOpened():
		print(f'Failed to open video file: {videoFilename}')
		return

	print(f'Started {videoFilename}')
	for frameObj in iterateVideo(video):
		frameImg = frameObj['img']
		frameIndex = frameObj['index']

		for roi in textRegions:
			img = crop(frameImg, roi.rect)
			txt = sanitize(pytesseract.image_to_string(img))
			#print(f'{frameIndex}: {roi.name} = {txt}')
			out_filename = f'{Path(videoFilename).name}.{frameIndex}.png'
			out_path = out_dir / roi.name / txt / out_filename
			try:
				os.makedirs(out_path.parent, exist_ok = True)
				write_success = cv.imwrite(str(out_path), img)
			except:
				write_success = False
			if not write_success:
				os.makedirs(out_dir, exist_ok = True)
				f = open(f'{out_dir}/failed_writes.txt', mode='a')
				f.write(f'{out_path}\n')
				f.close()
	print(f'Completed {videoFilename}')


### DRIVER CODE
if len(sys.argv) < 2:
	print('usage: gen_training_data.py file1 file2 file3...')

for videoFilename in sys.argv[1:]:
	gen_training_data(videoFilename)
