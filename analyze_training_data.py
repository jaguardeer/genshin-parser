import os
from pprint import pprint

sample_dir = './training-data/substat/CRITDMG+13.2%'
filenames = os.listdir(sample_dir)

parts = [f.split('.') for f in filenames]

# check if filenames match expected formats
import re
r = re.compile('^\\d+$')
pprint([p for p in parts if p[1] != 'mkv'])
pprint([p for p in parts if not r.match(p[2])])
pprint([p for p in parts if p[3] != 'png'])


# group imgs by p[0]
import itertools
def getname(x):
	return x[0]
parts.sort(key = getname)
groups = {k: list(g) for k, g in itertools.groupby(parts, getname)}


# do min/max operations
import cv2 as cv
import numpy as np
for key, img_list in groups.items():
	imgs_bgr = [cv.imread(f"{sample_dir}/{'.'.join(x)}") for x in img_list]
	imgs_hsv = [cv.cvtColor(x, cv.COLOR_BGR2HSV) for x in imgs_bgr]

	min_hsv = np.min(imgs_hsv, axis = 0)
	max_hsv = np.max(imgs_hsv, axis = 0)
	min_bgr = np.min(imgs_bgr, axis = 0)
	max_bgr = np.max(imgs_bgr, axis = 0)

	cv.imwrite(f'{key}_min_bgr.png', min_bgr)
	cv.imwrite(f'{key}_max_bgr.png', max_bgr)
	cv.imwrite(f'{key}_min_hsv.png', min_hsv)
	cv.imwrite(f'{key}_max_hsv.png', max_hsv)
