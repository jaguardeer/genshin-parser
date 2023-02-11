from common import *
import pytesseract


## from controller-view.png:
## substatBullets g-value in 86 - 159
## setKey text g-value in 159 - 220
## todo: make this better? i'm literally checking 4 pixels
## could check if any pixels in 4x4 or so square match
def countSubstatLines(frame):
	col = 1376
	rows = range(443, 540, 32)
	numLines = next((i for i, x in enumerate(rows) if frame[x, col, 1] >= 128), len(rows))
	return numLines


if __name__ == '__main__':

	regions = [
		{'key': 'name', 'rect': (1343, 133, 408, 46)},
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

	for frameObj in iterateVideo(video):
		frameIndex = frameObj['index']
		frameImg = frameObj['img']

		validLines = 0
		for k in substatRegionKeys:
			img = crop(frameImg, next(r['rect'] for r in regions if r['key'] == k))
			text = pytesseract.image_to_string(img).strip()
			if isValidSubstatString(text): validLines += 1

		numLines = countSubstatLines(frameImg)
		#print(numLines, validLines)

		if numLines != validLines:
			print(f'line count mismatch on frame {frameIndex}: tess {validLines}, mine {numLines}')