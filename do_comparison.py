import cv2 as cv
import numpy as np
import common

sampleVideo = cv.VideoCapture('./sample-videos/2023-12-24 11-27-56-1440p-scaled.mkv')
sample = common.getFrame(sampleVideo, 1000)

left, top = 1396, 435
width, height = 245, 21
extraSpace, heightSpacing = 3, 32
substatRects = [(left - extraSpace, top - extraSpace + offset * heightSpacing,
	width + extraSpace * 2, height + extraSpace * 2)
	for offset in range(4)
]

sample = common.crop(sample, substatRects[3])

#min_img = cv.imread('./ranges/substat/CRITDMG+13.2%/min.png')
#max_img = cv.imread('./ranges/substat/CRITDMG+13.2%/max.png')

#min_img = cv.imread('./ranges/substat/CRITDMG+13.2%/min_gray.png')
#max_img = cv.imread('./ranges/substat/CRITDMG+13.2%/max_gray.png')
#sample = cv.cvtColor(sample, cv.COLOR_BGR2GRAY)
#sample = cv.cvtColor(sample, cv.COLOR_GRAY2BGR)

min_img = cv.imread('./ranges/substat/CRITDMG+13.2%/min_hsv.png')
max_img = cv.imread('./ranges/substat/CRITDMG+13.2%/max_hsv.png')
sample = cv.cvtColor(sample, cv.COLOR_BGR2HSV)


above_max = sample > max_img
below_min = sample < min_img

out_of_range_c3 = np.logical_or(above_max, below_min)
out_of_range = np.any(out_of_range_c3, axis = 2)

sample2 = sample.copy()
ys, xs = np.where(out_of_range)
for y, x in zip(ys, xs):
	sample2[y, x] = out_of_range_c3[y, x] * 255
	#print(i)

ys, xs = np.where(np.any(above_max, axis = 2))
for y, x in zip(ys, xs):
	print(f'{x}, {y}: {sample[y, x] - max_img[y, x]}')

ys, xs = np.where(np.any(below_min, axis = 2))
for y, x in zip(ys, xs):
	print(f'{x}, {y}: {min_img[y, x] - sample[y, x]}')


cv.imshow('out_of_range_c3', out_of_range_c3 * 1.0)
cv.imshow('above_max', above_max * 1.0)
cv.imshow('below_min', below_min * 1.0)
cv.imshow('sample', sample)
cv.imshow('sample2', sample2)
cv.imshow('min_img', min_img)
cv.imshow('max_img', max_img)

minmaxdiff = max_img - min_img
minmaxnorm = (minmaxdiff / np.max(minmaxdiff) * 255).astype(np.uint8)

cv.imshow('minmaxnorm', minmaxnorm)
cv.imwrite('minmaxnorm.png', minmaxnorm)
cv.imwrite('minmaxdiff.png', minmaxdiff)

cv.waitKey()