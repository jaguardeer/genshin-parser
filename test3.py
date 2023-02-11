import cv2 as cv
import numpy as np

## TODO: proper channels
def getVideoShape(video):
	width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
	height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
	return height, width, 3

## frameSkipTest(curr, prev) -> return True if frame should be skipped
## todo: frameSkipTest(frame) and then use static local prev in func?
## todo: preallocating buffer breaks stuff, loss of precision?
def iterateVideo(video, frameSkipTest = lambda curr, prev: False):
	frameIndex = 0
	while True:
		success, curFrame = video.read()
		if not success: break
		if frameIndex == 0 or not frameSkipTest(curFrame, prevFrame):
			yield {'index': frameIndex, 'img': curFrame}
		frameIndex += 1
		prevFrame = curFrame


if __name__ == '__main__':
	video1 = cv.VideoCapture('2023-01-15 17-48-41.mp4')
	video2 = cv.VideoCapture('2023-01-15 17-48-41.mp4')

	buffer = np.empty(getVideoShape(video2), np.uint8)
	for x in range(100):
		success1, frame1 = video1.read()

	while True:
		success1, frame1 = video1.read()
		success2, frame2 = video2.read()
		diff = frame2 - frame1

		diffs = cv.countNonZero(cv.cvtColor(diff, cv.COLOR_BGR2GRAY))
		if diffs != 0:
			print(diffs)

		cv.imshow('frame1', frame1)
		cv.imshow('frame2', frame2)
		cv.imshow('diff', diff)
		cv.waitKey(1)