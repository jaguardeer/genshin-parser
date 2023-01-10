import cv2 as cv
import numpy as np
import time

## GLOBALS
#load video
video = cv.VideoCapture("./stream.mkv")

def main():
	# init output array
	width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
	sumFrame = np.zeros((height, width), dtype = np.int32)
	# for each frame of video
	i = 0
	while True:
		i += 1
		success, vidFrame = video.read()
		if not success: break
		vidFrame = cv.cvtColor(vidFrame, cv.COLOR_RGB2GRAY)
		#print(vidFrame.shape)
		sumFrame += vidFrame

	avgFrame = sumFrame / i
	cv.imwrite("average.png", avgFrame)
	cv.imshow("average", avgFrame)
	cv.waitKey()

def binarize(img):
	result, imgBinary = cv.threshold(img, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)


## Only run main if not in -i and not imported
import sys
if sys.flags.interactive == 0 and __name__ == "__main__" : main()