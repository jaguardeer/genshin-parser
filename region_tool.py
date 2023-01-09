import argparse
from ocr_video import *

regions = [
	"name",
	"slot",
	"mainstat_name",
	"mainstat_value",
	"level",
	"sub1",
	"sub2",
	"sub3",
	"sub4",
]

def makeRegions(regionFile):
	(success, frame_img) = video.read()

	output = {}

	for region in regions:
		r = cv.selectROI(region, arti_img, showCrosshair = True, fromCenter = False)
		output[region] = [int(r[1]), int(r[1]+r[3]), int(r[0]), int(r[0]+r[2])]

	outStr = json.dumps(output, sort_keys=True, indent=4)
	print(outStr)
	f = open(regionFile, "w")
	f.write(outStr)
	f.close()

def drawRegions(regionFile):
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

def main():
	parser = argparse.ArgumentParser(
		prog = 'Artifact Region Tool',
		description = 'Set or draw artifact regions.')
	parser.add_argument('filename')     # positional argument
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-d', '--draw', action = "store_true", help = "Draw regions") # option that takes a value
	group.add_argument('-s', '--set', action = "store_true", help = "Set regions")  # on/off flag
	#parser.add_argument('-i', '--image', help = "Image to use", default = )
	args = parser.parse_args()

	if args.draw: drawRegions(args.filename)
	if args.set: makeRegions(args.filename)


if __name__ == "__main__": main()