import urllib.request
import sys
from html.parser import HTMLParser
from bs4 import BeautifulSoup

def readURL(url):
	try:
		response = urllib.request.urlopen(url)
		if response.msg != 'OK':
			raise
		return response.read()
	except:
		return None


# get artifact set wiki page
artifact_wiki_url = "https://genshin-impact.fandom.com/wiki/Artifact/Sets"
html = readURL(artifact_wiki_url)
print(f"Reading wiki at {artifact_wiki_url}")
if html == None:
	print(f"Couldn't read URL: {artifact_wiki_url}")
	exit()
artifact_set_page = BeautifulSoup(html, features="html.parser")


# get artifact set table from page
table = artifact_set_page.table # artifact table is (probably) first table on page
# validate table
def sanitize(string):
	def is_allowed(c):
		allowed = '_'
		return c.isalnum() or c in allowed
	return ''.join(c.lower() for c in string if is_allowed(c))
header = [sanitize(i.get_text()) for i in table.find_all('th')]
expected_header = ['set', 'rarity', 'pieces', 'bonuses']
if header != expected_header:
	print("Got unexpected table header from wiki. Exiting...")
	exit()


# parse table
table_rows = [row.find_all('td') for row in table.find_all('tr') if row.td != None]

from strKeyDicts import SET_KEY_STRINGS, NAME_SET_SLOT_KEY_STRINGS

def to_pascal(name):
	return ''.join(c for c in ''.join(word.capitalize()
		for word in name.split(' '))
		if c.isalnum())

slotKeys = ['flower', 'plume', 'sands', 'goblet', 'circlet']
item2setslot = {
	piece: {'setKey': to_pascal(name.get_text()), 'slotKey': slotKey}
	for name, rarity, pieces, bonuses in table_rows
	for piece, slotKey in zip({to_pascal(p.get('alt')) for p in pieces.find_all('img')}, slotKeys)
}