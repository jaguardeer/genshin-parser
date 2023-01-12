from util import *

# values ending in 5 might be rounded differently in python than in game
def genUniqueSums(numbers, maxDepth, roundFunc):
	sums = [{0}] * (maxDepth + 1)
	for i in range(1, maxDepth + 1):
		sums[i] = {x + y for x in sums[i-1] for y in numbers}
	roundSums = map(lambda row: {roundFunc(x) for x in row}, sums)
	return roundSums

def mapFunc(key):
	return set().union(*list(genUniqueSums(substats[key], 6, getRoundFunc(key))))

def getRoundFunc(statKey):
	return (lambda x: round(x * 100, 1)) if statKey.endswith("_") else (lambda x: round(x))


substats = loadJsonFile("./artifact-stats.json")[0]["substats"]

numberSets = set().union(*map(lambda k: set.union(*genUniqueSums(substats[k], 6, getRoundFunc(k))), substats.keys()))

SUBSTAT_KEY_STRINGS = {
	"hp": ("HP", ""),
	"hp_": ("HP", "%"),
	"atk": ("ATK", ""),
	"atk_": ("ATK", "%"),
	"def": ("DEF", ""),
	"def_": ("DEF", "%"),
	"critRate_": ("CRIT Rate", "%"),
	"critDMG_": ("CRIT DMG", "%"),
	"enerRech_": ("Energy Recharge", "%"),
	"eleMas": ("Elemental Mastery", ""),
}


from gen_font_image import *

## text config
# 24 seems to be a good value
fontSize = 24
fontPath = "./zh-cn.ttf"
font = ImageFont.truetype(fontPath, fontSize)
gray = (92, 77, 71)
cream = (215, 228, 233)

for item in SUBSTAT_KEY_STRINGS.items():
	key = item[0]
	depth = 6
	values = set().union(*list(genUniqueSums(substats[key], depth, getRoundFunc(key)))[1:])
	prefix = item[1][0]
	suffix = item[1][1]

	print(prefix, suffix)
	print(values)

	for v in values:
		string = f"{prefix}+{v}{suffix}"
		img = createTemplate(string, font, gray, cream)
		cv.imwrite(f"templates/{string}.png", img)
