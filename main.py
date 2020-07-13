# Chandler Mahkorn 7/12/20 - 11:18 PM
import aiohttp
import asyncio
import Constants
import json
import PokeOBJ

async def main():
	try:
		testObj = PokeOBJ.PokeOBJ('.gen7 shiny primarina')
		print(testObj)

	except PokeOBJ.PokeError as err:
		print(err)

	async with aiohttp.ClientSession() as session:
		# Get species' typing
		async with session.get('https://pokeapi.co/api/v2/pokemon/' + testObj.getSpecies()) as resp:
			if resp.status == 200:
				speciesInfo = await resp.json()

				# Get species' type(s)
				speciesTypes = []
				speciesTypes.append(speciesInfo['types'][0]['type']['name'])
				if (len(speciesInfo['types']) > 1):
					speciesTypes.append(speciesInfo['types'][1]['type']['name'])

				print('Types: %s' % str(speciesTypes))
					
		# Get species' dex entry
		async with session.get('https://pokeapi.co/api/v2/pokemon-species/' + testObj.getSpecies() ) as resp:
			if resp.status == 200:
				dexInfo = await resp.json()
				dexEntries = dexInfo['flavor_text_entries']
				speciesEntry = ''

				# Find the closest entry for the given generation
				# Does not care about which game, just if it's the right gen
				for entry in dexEntries:
					if (entry['language']['name'] == 'en'):
						if (Constants.DICT_VERSION[entry['version']['name']] == Constants.DICT_GEN[testObj.getGen()]):
							speciesEntry = entry['flavor_text'].replace('\n', ' ')
							break

				print('Entry: %s' % speciesEntry)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())