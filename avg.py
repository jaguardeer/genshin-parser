from common import *

import cv2 as cv
import numpy as np

if __name__ == '__main__':
	video = cv.VideoCapture('2023-01-15 17-48-41.mp4')

	sums = np.zeros((1080, 1920, 3), np.uint32)
	curMax = np.zeros((1080, 1920), np.uint8)
	curMin = np.full((1080, 1920), 255, np.uint8)
	for frameObj in iterateVideo(video):
		img = frameObj['img']
		gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
		curMax = np.maximum(curMax, gray)
		curMin = np.minimum(curMin, gray)
		sums += img

	#sums /= 10970
	framesAvg = sums / 10970

	cv.imwrite('avg.png', framesAvg)
	cv.imwrite('max.png', curMax)
	cv.imwrite('min.png', curMin)
