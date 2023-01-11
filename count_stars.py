import cv2 as cv
import numpy as np
import time

start = time.time()

## todo: match on binarized version
img_rgb = cv.imread('artifact-page.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('test-template.png', 0)
#mask = cv.imread('res2.png', 0)

loadTime = time.time()

w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

matchTime = time.time()

## multiple matching
threshold = 0.97
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
	cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + yyh), (0,0,255), 2)

drawTime = time.time()


## best fit matching
minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(res)

findTime = time.time()

pt = maxLoc
print(maxVal)
cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)


## write results
cv.imwrite('res.png',img_rgb)
print(len(list(zip(*loc[::-1]))))

end = time.time()
