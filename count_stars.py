import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv.imread('artifact-page.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('star-template.png', 0)
mask = cv.imread('res2.png', 0)

w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED, mask = mask)
threshold = 0.97
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
	cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imwrite('res.png',img_rgb)
print(len(list(zip(*loc[::-1]))))