import cv2 as cv
import pytesseract
from common import *




def charIsAllowed(char):
	otherAllowed = [' ', '_', '.', '+']
	if char.isalnum():
		return True
	else:
		return char in otherAllowed

def strToFilename(string):
	string = string.replace('%', '_')
	for c in string:
		if not charIsAllowed(c):
			string = string.replace(c, '')
	return string





if __name__ == '__main__':
	import os
	groups = {
		#'icon': 
		'mainstat': [(1356, 253, 200, 28)],
		#'mainstat': [(1356, 253, 183, 28)],
		#'rarity': [(1356, 323, 157, 36)],
		'level': [(1370, 391, 42, 20)],
		'substats': [(1382, 428, 260, 30), (1382, 460, 260, 32), (1382, 491, 260, 34), (1383, 522, 260, 37)]
	}

	outDir = './sift'
	vidFilename = '2023-01-15 17-48-41.mp4'
	video = cv.VideoCapture(vidFilename)
	for frameObj in iterateVideo(video):
		for key, regionList in groups.items():
			for rect in regionList:
				frameIndex = frameObj['index']
				img = crop(frameObj['img'], rect)
				_, imgBin = cv.threshold(img[:, :, 0], 128, 255, cv.THRESH_BINARY)
				bb = cv.boundingRect(imgBin)
				imgCr = crop(img, (0, 0, bb[0]+bb[2]+8, img.shape[0]))
				imageString = pytesseract.image_to_string(imgCr)
				if False:#imageString == '':
					print(f'None for {key}')
					cv.imshow(key, img)
					cv.imshow(key+' bin', imgCr)
					cv.waitKey()
					exit()
				fileDir = f'{outDir}/{key}/{strToFilename(imageString)}'
				os.makedirs(fileDir, exist_ok = True)
				fileIndex = len(os.listdir(fileDir))
				filename = f'{fileDir}/{vidFilename}.{frameIndex}.png'
				cv.imwrite(filename, img)