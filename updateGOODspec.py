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



artifact_wiki_url = "https://genshin-impact.fandom.com/wiki/Artifact/Sets"
html = readURL(artifact_wiki_url)
print(f"Reading wiki at {artifact_wiki_url}")
if html == None:
	print(f"Couldn't read URL: {artifact_wiki_url}")
	exit()


def sanitize(string):
	def is_allowed(c):
		allowed = '_'
		return c.isalnum() or c in allowed
	return ''.join(c.lower() for c in string if is_allowed(c))

bs = BeautifulSoup(readURL("https://genshin-impact.fandom.com/wiki/Artifact/Sets"), features="html.parser")

table = bs.table # artifact table is (probably) first table on page
# validate table
header = [sanitize(i.get_text()) for i in table.find_all('th')]
expected_header = ['set', 'rarity', 'pieces', 'bonuses']
if header != expected_header:
	print("Got unexpected table header from wiki. Exiting...")
	exit()


data = [row.find_all('td') for row in table.find_all('tr') if row.td != None]


for i in data:
	name, rarity, pieces, bonuses = (x.get_text() for x in i)
	print(f'Name: {i[0]}')