import json

SUBSTAT_KEY_STRINGS = {
	"HP": "hp",
	"ATK": "atk",
	"DEF": "def",
	"CRIT Rate": "critRate",
	"CRIT DMG": "critDMG",
	"Energy Recharge": "enerRech",
	"Elemental Mastery": "eleMas",
}

def raw2goodMainstat(rawStr):
    return

## todo: error checking / validation?
def raw2goodSubstat(rawStr):
    namePart, valPart = rawStr.split("+")
    key = SUBSTAT_KEY_STRINGS[namePart] + ("_" if valPart.endswith("%") else "")
    val = valPart.rstrip("%")
    return key, val



## GOOD format wants:
## -- setKey
## -- rarity
## -- level
## -- mainStatKey
## -- substats
## -- optional: location, exclude, lock, id
## genshin optimizer will accept invalid artifacts (wrong substats f. ex)
