import pytesseract
import cv2
import sys

if len(sys.argv) < 2:
	print("Specify file to read")
	exit()

fn = sys.argv[1]
img = cv2.imread(fn)
hImg, wImg, _ = img.shape

configStr = ""
string = pytesseract.image_to_string(img, config = configStr)
print(string)
boxes = pytesseract.image_to_boxes(img, config = configStr)
print(boxes)
for b in boxes.splitlines():
	b = b.split(' ')
	x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
	cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
	cv2.putText(img, b[0], (x, hImg - y + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 205, 50), 1)

#data = pytesseract.image_to_data(img, config = configStr)
#print(data)


cv2.imshow('Detected text', img)
cv2.waitKey(0)