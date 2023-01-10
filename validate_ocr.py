from util import *
import re

MAINSTAT_KEY_STRINGS = {
	"HP": "",
	"ATK": "",
	"DEF": "",
	"CRIT Rate": "",
	"CRIT DMG": "",
	"Energy Recharge": "",
	"Healing Bonus": "",
	"Elemental Mastery": "",
	"Physical DMG Bonus": "",
	"Anemo DMG Bonus": "",
	"Geo DMG Bonus": "",
	"Electro DMG Bonus": "",
	"Hydro DMG Bonus": "",
	"Pyro DMG Bonus": "",
	"Cryo DMG Bonus": "",
	"Dendro DMG Bonus": "",
}

SUBSTAT_KEY_STRINGS = {
	"HP": "hp",
	"ATK": "atk",
	"DEF": "def",
	"CRIT Rate": "critRate",
	"CRIT DMG": "critDMG",
	"Energy Recharge": "enerRech",
	"Elemental Mastery": "eleMas",
}

SLOT_KEY_STRINGS = {
	"Flower of Life": "flower",
	"Plume of Death": "plume",
	"Sands of Eon": "sands",
	"Goblet of Eonothem": "goblet",
	"Circlet of Logos": "circlet",
}

ARTIFACT_SETS = loadJsonFile("artifact-sets.json")

## todo: validate against set?
## also todo: rearrange artifact-sets.json to dict of {setName: {goblet: "asda", ...}}
def validateNameString(nameString):
	return any(map(lambda artiSet: nameString in artiSet.values(), ARTIFACT_SETS))

def validateLevelString(levelString):
	pattern = "\\+[0-9]+"
	return re.fullmatch(pattern, levelString) and int(levelString) in range(21)

def validateSlotString(slotString):
	return slotString in SLOT_KEY_STRINGS.keys()

def validateMainstatString(mainstatString):
	return mainstatString in MAINSTAT_KEY_STRINGS.keys()

## check that substat string (ex: "ATK+4.1%") matches KEY+VALUE format
def validateSubstatString(substatString):
	keyPattern = "(?:" + "|".join(SUBSTAT_KEY_STRINGS.keys()) + ")"
	pattern = keyPattern + "\\+(?:[0-9],)?[0-9]+(?:\\.[0-9]%)?"
	return None != re.fullmatch(pattern, substatString)

## todo: count rolls, etc
def validateResult(ocrResult):
	funcTable = {
		"name": validateNameString,
		"level": validateLevelString,
		"mainstat_name": validateMainstatString,
		"slot": validateSlotString,
		"sub1": validateSubstatString,
		"sub2": validateSubstatString,
		"sub3": validateSubstatString,
		"sub4": validateSubstatString,
	}
	## refactor to return any(map()) or something
	for key, val in ocrResult.items():
		val = val.strip("\n")
		valid = funcTable[key](val)
		if not valid:
			print(f"invalid result: {val}")
			return False
	return True