import os
from pathlib import Path

field_names = 'level', 'mainstat', 'name', 'substat'

data_dir = Path('./training-data')
out_dir = Path('./ranges')

dirs = [Path(x) / y for x in field_names for y in os.listdir(data_dir / x)]


import numpy as np
import cv2 as cv


def write_img(path, img):
	os.makedirs(path.parent, exist_ok = True)
	success = cv.imwrite(str(path), img)
	if not success:
		print(f'Failed to write {str(path)}')

for d in dirs:
	dirname = data_dir / d
	files =  [dirname / x for x in os.listdir(dirname)]
	imgs = [cv.imread(str(x)) for x in files]
	min_bgr = np.min(imgs, axis = 0)
	max_bgr = np.max(imgs, axis = 0)
	imgs_hsv = [cv.cvtColor(x, cv.COLOR_BGR2HSV) for x in imgs]
	min_hsv = np.min(imgs_hsv, axis = 0)
	max_hsv = np.max(imgs_hsv, axis = 0)

	write_img(out_dir / d / 'min_gray.png', min_bgr)
	write_img(out_dir / d / 'max_gray.png', max_bgr)
	write_img(out_dir / d / 'min_gray.png', min_hsv)
	write_img(out_dir / d / 'max_gray.png', max_hsv)

	imgs = [cv.imread(str(x)) for x in files]
	imgs_bgr = {'tag': 'bgr', 'imgs': imgs}
	imgs_hsv = {'tag': 'hsv', 'imgs': [cv.cvtColor(x, cv.COLOR_BGR2HSV) for x in imgs]}