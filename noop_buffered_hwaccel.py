import sys
import cv2 as cv
import numpy as np

if len(sys.argv) != 2:
	print('usage: python noop.py filename')
	exit()


videoFilename = sys.argv[1]

video = cv.VideoCapture(videoFilename, cv.CAP_ANY, [cv.CAP_PROP_HW_ACCELERATION, cv.VIDEO_ACCELERATION_ANY])#, cv.CAP_PROP_HW_ACCELERATION_USE_OPENCL, 1])

if not video.isOpened():
	print(f'Failed to open {videoFilename}')
	exit()

h , w = [int(video.get(x)) for x in (cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FRAME_WIDTH)]

buffer = np.empty((h, w), np.uint8)
success, frame = video.read(buffer)
while success:
	#cv.imshow('test', frame)
	#cv.waitKey(1)
	success, frame = video.read(buffer)
