from ocr3 import *


video = cv.VideoCapture('2023-01-15 15-31-44.mp4')

def imageToString(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	#img = cv.dilate(img, np.ones((2, 2), np.uint8))
	#cv.imshow('b', img)
	#cv.waitKey()
	#_, img = cv.threshold(img, 140, 255, cv.THRESH_BINARY)
	#img = cv.medianBlur(img, 3)
	txt = pytesseract.image_to_string(img)
	cv.imshow('a', img)
	return txt.strip()


## takes frame, returns {mainStatKey}
mainStatImgCache = []
def parseMainStat(frame):
	#mainStatRegion = (1360, 257, 199, 26)
	mainStatRegion = (1365, 253, 200, 30)
	img = crop(frame, mainStatRegion)
	## Check cache, parse and add new entry if no match
	global mainStatImgCache
	cacheMatches = (x for x in mainStatImgCache if isSameMainstatImg(img, x['img']))
	cacheResult = next(cacheMatches, None)
	if not cacheResult:
		strResult = imageToString(img)
		mainStatImgCache.append({'strResult': strResult, 'img': np.copy(img)}) ## does img need copy?
	else:
		strResult = cacheResult['strResult']
	## (optional) Check if extra matches just to be safe
	for extraMatch in cacheMatches:
		print(f'extra match for {strResult}')
		cv.imshow('orig', img)
		cv.imshow('cached', extraMatch['img'])
		cv.waitKey()
	return {'mainStatKey': strResult}

frames = [362, 1636, 1811, 2278, 3137, 3755, 3776, 9014, 9021, 9041, 9076] 

for fi in frames:
	frame = getFrame(video, fi)
	result = parseMainStat(frame)
	#txt = pytesseract.image_to_string(frame)
	print(result)
	#cv.imshow('test', frame)
	cv.waitKey()