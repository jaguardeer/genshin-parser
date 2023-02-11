from common import *
import pytesseract

frames = [1375, 1375, 4197, 4197, 4203, 4203, 4209, 4209, 4215, 4215, 7690, 7690, 7697, 7697, 7703, 7703, 7710, 7710]


video = cv.VideoCapture('2023-01-15 17-48-41.mp4')
for fi in frames:
	frame = getFrame(video, fi)
	region = (1365, 136, 361, 40)
	cropped = crop(frame, region)
	nameImg = cv.copyMakeBorder(cropped, 5, 5, 5, 5, cv.BORDER_CONSTANT, value = cropped[-1, -1].tolist())
	txt = pytesseract.image_to_string(nameImg)
	print(stripNonAlpha(txt))
	frame = cv.rectangle(frame, (region[0], region[1]), (region[0] + region[2], region[1] + region[3]), (255, 255, 0), thickness = 1)
	cv.imshow('f', frame)
	cv.imshow('f2', nameImg)
	cv.waitKey()