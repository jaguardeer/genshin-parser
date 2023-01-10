import json

def loadJsonFile(filename):
	f = open(filename)
	obj = json.load(f)
	f.close()
	return obj