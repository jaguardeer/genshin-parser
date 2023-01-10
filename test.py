import time
import numpy as np
import cv2 as cv


def defaultAlloc():
	video = cv.VideoCapture("./stream.mkv")
	while True:
		success, frame = video.read()
		if not success: break
		x = 2 + 2

def getVideoShape(video):
	width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
	return height, width, 3

def preAlloc():
	video = cv.VideoCapture("./stream2.mkv")
	frameBuffer = np.empty(getVideoShape(video), np.uint8)
	while video.read(frameBuffer)[0]:
		x = 2 + 2


start = time.time()
defaultAlloc()
end = time.time()
print(f"default allocation: {end - start}")

start = time.time()
preAlloc()
end = time.time()
print(f"pre allocation: {end - start}")