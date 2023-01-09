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


## Validate / correct OCR output:
##	- name
## 		- must exist in list
##		- must match slot & set
##	- slot
##		- must exist in set
##		- must match name
##	- mainstat_name
##		- must exist in list
##		- list depends on slot
##	- mainstat_value
##		- must match mainstat_name and level (lookup table)
##	- rarity
##		- value from 1-5
##	- level
##		- value from +0 to +20
##	- substats
##		- must exist as NAME+VALUE string
##		- NAME must be in list, can't match mainstat_name
##		- VALUE must exist as combination of rolls
##	- set_name
##		- must exist in list, match name
##	- set effects
## 		- must match set_name



## NEEDED FUNCS FOR TESSERACT TRAINING
## -- draw boxes