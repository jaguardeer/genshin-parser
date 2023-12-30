import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys

filename = sys.argv[1]
img = cv.imread(filename)
assert img is not None, "file could not be read, check with os.path.exists()"

from common import crop
roi = cv.selectROI('selector', img)
img = crop(img, roi)

color = ('b','g','r')
for i, col in enumerate(color):
    histr = cv.calcHist([img],[i],None,[256],[0,256])
    #plt.plot(histr, color = col)
    plt.bar(range(256), histr.ravel(), width = 1, color = col)
    plt.xlim([0,255])
    plt.title(filename)
plt.show()