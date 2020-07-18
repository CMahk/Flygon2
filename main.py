import aiohttp
import asyncio
import Constants
import json
import os
import sqlite3
import PokeOBJ

path = os.path.abspath(os.path.dirname(__file__))

async def main():
	try:
		testObj = PokeOBJ.PokeOBJ('.gen6 shiny mega venusaur')
		print(testObj)

	except PokeOBJ.PokeError as err:
		print(err)

	#async with aiohttp.ClientSession() as session:
	#	# Get species' typing
	#	async with session.get('https://pokeapi.co/api/v2/pokemon/' + testObj.getSpecies()) as resp:
	#		if resp.status == 200:
	#			speciesInfo = await resp.json()

	#			# Get species' type(s)
	#			speciesTypes = []
	#			speciesTypes.append(speciesInfo['types'][0]['type']['name'])
	#			if (len(speciesInfo['types']) > 1):
	#				speciesTypes.append(speciesInfo['types'][1]['type']['name'])

	#			print('Types: %s' % str(speciesTypes))

	## Get species' dex entry
	#async with session.get('https://pokeapi.co/api/v2/pokemon-species/' + testObj.getSpecies() ) as resp:
	#	if resp.status == 200:
	#		dexInfo = await resp.json()
	#		dexEntries = dexInfo['flavor_text_entries']
	#		speciesEntry = ''

	#		# Find the closest entry for the given generation
	#		# Does not care about which game, just if it's the right gen
	#		for entry in dexEntries:
	#			if (entry['language']['name'] == 'en'):
	#				if (Constants.DICT_VERSION[entry['version']['name']] == Constants.DICT_GEN[testObj.getGen()]):
	#					speciesEntry = entry['flavor_text'].replace('\n', ' ')
	#					break

	#		print('Entry: %s' % speciesEntry)
					
	db = sqlite3.connect(path + '\\Poke.db')
	cursor = db.cursor()

	cursor.execute('SELECT * FROM pokemon WHERE species LIKE ?', (testObj.getSpecies(),))

	# Get the species' dex number
	speciesDex = list(cursor.fetchone())[0]

	version = Constants.DICT_DEFAULT_VERSION[testObj.getGen()]

	# 9 = English language
	cursor.execute('SELECT * FROM pokedex WHERE species LIKE ? AND version LIKE ? AND language LIKE ?', (speciesDex, version, 9))
	text = list(cursor.fetchone())[4]
	print(text)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())