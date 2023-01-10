import json
import re

def loadJsonFile(filename):
	file = open(filename)
	result = json.load(file)
	file.close()
	return result

ARTIFACT_STATS = loadJsonFile("artifact-stats.json")
MAINSTAT_KEYS = ARTIFACT_STATS[0]["mainstats"].keys()
SUBSTAT_KEYS = ARTIFACT_STATS[0]["substats"].keys()

SUBSTAT_KEY_STRINGS = {
	"HP": "hp",
	"ATK": "atk",
	"DEF": "def",
	"CRIT Rate": "critRate",
	"CRIT DMG": "critDMG",
	"Energy Recharge": "enerRech",
	"Elemental Mastery": "eleMas"
}


## (unused) can do further validation...# of digits, percent or int only, etc
FLAT_ONLY = ["Elemental Mastery"]
PERCENT_ONLY = ["Energy Recharge", "CRIT Rate", "CRIT DMG"]
FLAT_OR_PERCENT = ["HP", "ATK", "DEF"]

def validateSubstatKey(substatKey):
	return substatKey in SUBSTAT_KEYS

## check regex (depends on key), check if can sum with rolls
def validateSubstatValue(substatValue, substatKey, maxRolls):
	return 

## check that substat string (ex: "ATK+4.1%") matches KEY+VALUE format
def validateSubstatString(substatString):
	keyPattern = "(?:" + "|".join(SUBSTAT_KEY_STRINGS.keys()) + ")"
	pattern = keyPattern + "\\+[0-9]+(?:\\.[0-9]%)?"
	return None != re.fullmatch(pattern, substatString)

def getSubstatKey(keyStr, valueStr):
	base = SUBSTAT_KEY_STRINGS[keyStr]
	percent = "_" if valueStr.endswith("%") else ""
	return base + percent

## ocr output might be valid, invalid, or unparseable
def parseSubstatOCR(ocrSubstat, artifactLevel = 0):
	## return None if can't parse
	stringOK = validateSubstatString(ocrSubstat)
	if not stringOK: return None
	## parse substat
	keyStr, valueStr = ocrSubstat.split("+")
	key = getSubstatKey(keyStr, valueStr)
	value = float(valueStr.rstrip("%"))
	return (key, value, rolls)

## returns number of rolls to make a sum
def canSum(targetSum, numbers, depth = 0):
	#print("checking",round(targetSum, 1),"vs",numbers,"at depth",maxNumbers)
	if round(targetSum, 1) == 0: return True
	elif targetSum < 0 or maxNumbers == 0: return False
	else: return any(map(lambda x: canSum(targetSum - x * 100, numbers, maxNumbers - 1), numbers))

# todo: supply a roundFunc instead of args to pass to round()
# values ending in 5 might be rounded differently in python than in game
def allValues(numbers, maxDepth = 1, places = 0, multi = 1):
    exacts = [{0}] * (maxDepth + 1)
    for i in range(1, maxDepth + 1):
       exacts[i] = {x + y for x in exacts[i-1] for y in numbers}
    rounded = map(lambda row: {round(x * multi, places) for x in row}, exacts)
    return rounded

def mapFunc(key):
    if key.endswith("_"):
        multi = 100
        places = 1
    else:
        multi = 1
        places = 0
    return set().union(*list(allValues(ARTIFACT_STATS[0]["substats"][key], 6, places, multi)))

print(parseSubstatOCR("ATK+4.1%", 5))
print(parseSubstatOCR("ATK+S5.1%", 5))
print(parseSubstatOCR("ATTK+4.1%", 5))


