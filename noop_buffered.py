import sys
import cv2 as cv
import numpy as np

if len(sys.argv) != 2:
	print('usage: python noop.py filename')
	exit()


videoFilename = sys.argv[1]

video = cv.VideoCapture(videoFilename)

if not video.isOpened():
	print(f'Failed to open {videoFilename}')
	exit()

w = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
h = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))

buffer = np.empty((h, w, 3), np.uint8)

success, frame = video.read(buffer)
while success:
	#cv.imshow('test', frame)
	#cv.waitKey(1)
	success, frame = video.read(buffer)
