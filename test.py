from ocr_video import *

regionFile = "regions.json"

def makeRegions():
	(success, frame_img) = video.read()

	regions = ["name", "slot", "mainstat_name", "mainstat_value", "level", "sub1", "sub2", "sub3", "sub4"]

	output = {}

	r = cv.selectROI("full", frame_img, showCrosshair = True, fromCenter = False)
	output["full"] = [int(r[1]), int(r[1]+r[3]), int(r[0]), int(r[0]+r[2])]


	arti_img = frame_img[output["full"][0]:output["full"][1], output["full"][2]:output["full"][3]]
	for region in regions:
		r = cv.selectROI(region, arti_img, showCrosshair = True, fromCenter = False)
		output[region] = [int(r[1]), int(r[1]+r[3]), int(r[0]), int(r[0]+r[2])]

	outStr = json.dumps(output, sort_keys=True, indent=4)
	print(outStr)
	f = open(regionFile, "w")
	f.write(outStr)
	f.close()

def drawRegions():
	# load regions from json
	f = open(regionFile)
	regions = json.load(f)
	f.close()
	# load frame & crop
	(success, frame_img) = video.read()
	frame_cropped = frame_img[regions["full"][0]:regions["full"][1], regions["full"][2]:regions["full"][3]]
	# draw rects
	for rect in regions.values():
		cv.rectangle(frame_cropped, (rect[2], rect[0]), (rect[3], rect[1]), np.random.rand(3) * 255, 2)
		# cv.rectangle(frame_cropped, (region[2], region[0]), (region[3], region[1]), np.random.rand(3), 2)
	# show img
	cv.imshow("regions", frame_cropped)
	cv.waitKey()

drawRegions()