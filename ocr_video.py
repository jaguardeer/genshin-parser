import cv2 as cv
import pytesseract
import numpy as np
import json

## TODO: look into cv ROI
## cv pyramids
## use tesseract dll?
## TODO: collect errors and save to error log
## log what corrections were made
## log same frames
## todo: more corrections (stat names)


def loadJsonFile(filename):
	f = open(filename)
	obj = json.load(f)
	f.close()
	return obj

## GLOBALS
#load video
video = cv.VideoCapture("./stream.mkv")
artifactStats = loadJsonFile("./artifact-stats.json")[0]
regions = loadJsonFile("./regions.json")
arti_region = regions.pop("full")

## TODO: validate
def parseSubstat(substatStr):
	splits = substatStr.split("+")
	if len(splits) == 2: return {"name": splits[0], "value": splits[1]}
	else: return None

## TODO: make this nicer
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

## rounds mainstat_name string to closest match from list of possibilities
def lookupMainstat(mainstat_name):
	mainstats = artifactStats["mainstats"].keys()
	similarities = map(lambda x: (x, similar(x, mainstat_name)), mainstats)
	bestMatch = max(similarities, key = lambda x: x[1])[0]
	return bestMatch

## TODO: validate, lookup set name
def parseArtifact(ocrResult):
	msSuffix = "%" if ocrResult["mainstat_value"].endswith("%") else ""
	mainstat_name = lookupMainstat(ocrResult["mainstat_name"] + msSuffix)
	level = int(ocrResult["level"])
	sub1 = parseSubstat(ocrResult["sub1"])
	sub2 = parseSubstat(ocrResult["sub2"])
	sub3 = parseSubstat(ocrResult["sub3"])
	sub4 = parseSubstat(ocrResult["sub4"])

	artifact = {}
	artifact["name"] = ocrResult["name"]
	artifact["slot"] = ocrResult["slot"]
	artifact["level"] = ocrResult["level"]
	artifact["mainstat_name"] = mainstat_name
	artifact["mainstat_value"] = artifactStats["mainstats"][mainstat_name][level]
	artifact["substats"] = list(filter(lambda e: e != None, [sub1, sub2, sub3, sub4]))
	return artifact

def validateOcrResult():
	return None

## Parts of an artifact:
## - name
## - slot
## - mainstat_name
## - mainstat_value
## - rarity
## - level
## - substats
## - set_name
## - set_effects

def grabArtifactImg(frameImg):
	return cv.cvtColor(frameImg[arti_region[0]:arti_region[1], arti_region[2]:arti_region[3]], cv.COLOR_RGB2GRAY)

def calcFrameDifference(a, b):
	val = np.sum(cv.absdiff(a, b))
	#print(val)
	return val



def main():
	data_out = []
	i = -1;
	artifact_prev = {}
	img_prev = []
	frame_diff_threshold = 300_000 # kinda arbitrary, .5M seems good
	# for each frame of video
	while True:
		i = i + 1
		# grab frame, break if no frame
		(success, frame_img) = video.read()
		if not success:
			print("done")
			break

		# crop & greyscale
		frame_grey = grabArtifactImg(frame_img)

		# skip if frame is too similar to prev frame
		if i > 0:
			val = calcFrameDifference(img_prev, frame_grey)
			if(val < frame_diff_threshold):
				continue

		img_prev = frame_grey

		print("processing frame", i)
		"""
		# (debug) only first 200 frames
		if i > 200:
			break
		"""

		"""
		# (debug) print frame info
		print(frame_img.shape)
		cv.imwrite("./testout.png", frame_img)
		"""

		# set regions ## TODO: is this making copies?
		artifact_regions = {
			'name' : dict(img = frame_grey[regions['name'][0]:regions['name'][1], regions['name'][2]:regions['name'][3]], opts = ""),
			'slot' : dict(img = frame_grey[regions['slot'][0]:regions['slot'][1], regions['slot'][2]:regions['slot'][3]], opts = ""),
			'mainstat_name' : dict(img = frame_grey[regions['mainstat_name'][0]:regions['mainstat_name'][1], regions['mainstat_name'][2]:regions['mainstat_name'][3]], opts = ""),
			'mainstat_value' : dict(img = frame_grey[regions['mainstat_value'][0]:regions['mainstat_value'][1], regions['mainstat_value'][2]:regions['mainstat_value'][3]], opts = ""),
			'level' : dict(img = frame_grey[regions['level'][0]:regions['level'][1], regions['level'][2]:regions['level'][3]], opts = " --psm 13 "),
			'sub1' : dict(img = frame_grey[regions['sub1'][0]:regions['sub1'][1], regions['sub1'][2]:regions['sub1'][3]], opts = ""),
			'sub2' : dict(img = frame_grey[regions['sub2'][0]:regions['sub2'][1], regions['sub2'][2]:regions['sub2'][3]], opts = ""),
			'sub3' : dict(img = frame_grey[regions['sub3'][0]:regions['sub3'][1], regions['sub3'][2]:regions['sub3'][3]], opts = ""),
			'sub4' : dict(img = frame_grey[regions['sub4'][0]:regions['sub4'][1], regions['sub4'][2]:regions['sub4'][3]], opts = ""),
		}

		"""
		# (debug) show img
		cv.imshow("frame", frame_grey)
		cv.waitKey(0)
		"""

		artifact_out = {}

		# do OCR on each region
		for region in artifact_regions:
			imgNormal = artifact_regions[region]["img"]

			# process img
			erodeKernel = np.ones((2, 2), np.uint8)
			dilateKernel = np.ones((2, 2), np.uint8)
			imgNormal = cv.erode(imgNormal, erodeKernel, iterations=1)
			imgNormal = cv.dilate(imgNormal, dilateKernel, iterations=1)

			# upscale
			gray = cv.resize(imgNormal, None, fx=8, fy=8, interpolation=cv.INTER_CUBIC)

			# preprocess
			gray, img_bin = cv.threshold(gray,128,255,cv.THRESH_BINARY | cv.THRESH_OTSU)
			gray = cv.bitwise_not(img_bin)


			#run ocr
			text_out = pytesseract.image_to_string(gray, config=artifact_regions[region]["opts"])
			
			"""
			# (debug) display img
			cv.imshow("piece", gray)
			print(region,":", text_out)
			cv.waitKey()
			"""

			# write text
			directory = "./dbg/"
			artifact_out[region] = text_out.strip()
			fn = directory + str(i) + "-" + region
			cv.imwrite(fn + ".png", gray)
			txt = open(fn + ".txt", "w")
			txt.write(text_out.strip())
			txt.close()
			

		if artifact_out != artifact_prev:
			result = parseArtifact(artifact_out)
			data_out.append(result)
			print(json.dumps(result))
		else:
			print("Parsed same artifact, diff was", val)
			# frame_diff_threshold = val + 1

		artifact_prev = artifact_out

	print("Final frame_diff_threshold was", frame_diff_threshold)
	print("Final artifact count was", len(data_out))
	file_out = open("ocr-out.json", "w")
	json.dump(data_out, file_out, sort_keys=True, indent=4)
	file_out.close()



## Only run main if not in -i and not imported
import sys
if sys.flags.interactive == 0 and __name__ == "__main__" : main()