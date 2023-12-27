import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys

filename = sys.argv[1]
img = cv.imread(filename)
assert img is not None, f"Couldn't read {filename}"

h, w, c = img.shape
data = np.reshape(img, (h * w, c))
#print(img[0, 0])
#print(data[0])
#print(data.shape)
data = np.unique(data, axis = 0)
xs = data[:, 0]
ys = data[:, 1]
zs = data[:, 2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(xs, ys, zs)

ax.set_xlabel('R Channel')
ax.set_ylabel('G Channel')
ax.set_zlabel('B Channel')

plt.show()