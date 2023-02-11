from common import *
import subprocess
import itertools

def compareGoodFiles(fileA, fileB):
	artiLists = [loadJsonFile(x)['artifacts'] for x in [fileA, fileB]]
	## trim results to keys that I want to compare
	keys = ['level', 'substats', 'rarity', 'mainStatKey']
	trim = lambda arti: {k: arti[k] for k in keys}
	trimList = lambda l: [trim(x) for x in l]
	trimIntersect = lambda a, b: [x for x in a if trim(x) not in trimList(b)]
	## compare
	aNotB, bNotA = [trimIntersect(a, b) for a, b in itertools.permutations(artiLists)]

	return {'aNotB': aNotB, 'bNotA': bNotA}

def compareScanner(scanScript, videoFilename, expectedResultsFilename):
	## run ocr script, compare
	subprocess.run(['python', scanScript, videoFilename])
	scanResults = getResultsFilename(videoFilename, scanScript)
	wrong, missing = compareGoodFiles(scanResults, expectedResultsFilename).values()
	return {'wrong': wrong, 'missing': missing}


######  DRIVER CODE

if __name__ == '__main__':
	scripts = ['ocr3.py']
	videos = [
		'2023-01-15 17-48-41.mp4',
		'2023-01-15 15-31-44.mp4',
		'2023-01-29 16-09-59.mp4',
		'2023-02-10 21-03-43.mp4',
	]

	import time
	#compResults = [compareScanner(script, video, Path(video).with_suffix('.json')) for script, video in itertools.product(scripts, videos)]
	#for wrong, missing in compResults.values():
	#	print(f'num wrong: {len(compResults["wrong"])}')
	#	print(f'num missing: {len(compResults["missing"])}')

	results = []
	for script, video in itertools.product(scripts, videos):
		print(f'Testing {script} with {video}')
		startTime = time.time()
		expected = Path(video).with_suffix('.json')
		compResults = compareScanner(script, video, expected)
		print(f'Took {time.time() - startTime:.1f} seconds')
		print(f'num wrong: {len(compResults["wrong"])}')
		print(f'num missing: {len(compResults["missing"])}')
		info = {'script': script, 'video': video, 'results': compResults}
		results.append(info)
	