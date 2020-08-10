import aiosqlite
import aiofiles
import asyncio
import bisect
import json
import re
import os

class PokeDB():
	def __init__(this):
		this.path = os.path.abspath(os.path.dirname(__file__))
		this.db = None
		this.cursor = None

	# Close the database
	async def close(this):
		await this.db.close()

	async def setup(this):
		# Setup the db schema
		this.db = await aiosqlite.connect(this.path + '\\poke.db')
		this.cursor = await this.db.cursor()
		async with aiofiles.open(this.path + '\\schema.sql', 'r') as schema:
			await this.cursor.executescript(await schema.read())

		# Setup the db if it isn't already (see if the first row exists)
		await this.cursor.execute('SELECT * FROM pokemon WHERE dex LIKE ?', '1')
		check = await this.cursor.fetchone()
		if check is None:
			print('Database not found. Attempting to build one')
			print('Building pokemon table...')
			await this.__populatePokemon()

			print('Building pokedex table...')
			await this.__populatePokedex()

	async def __loadList(this, file):
		fileList = []
		async with aiofiles.open(this.path + '\\src\\' + file, 'r') as infile:
			async for line in infile:
				fileList.append(line.rstrip())

		return fileList

	async def __populatePokemon(this):
		# The list corresponds to: [species total for the generation, default game version, region, generation]
		# See Constants.DICT_VERSION_ID for specifics on what default game version is used to get flavor text
		dictIndex = {
			1: [151, 'kanto', 1],
			152: [251, 'johto', 2],
			252: [386, 'hoenn', 3],
			387: [493, 'sinnoh', 4],
			494: [649, 'unova', 5],
			650: [721, 'kalos', 6],
			722: [809, 'alola', 7],
			#TODO: Flavor text for SwSh
			810: [892, 'galar', 8]
			}

		# Load the files into lists
		listMega = await this.__loadList('mega.txt')
		listAlolan = await  this.__loadList('alolan.txt')
		listGalarian = await this.__loadList('galarian.txt')
		listGmax = await this.__loadList('gmax.txt')

		listFormes = []
		async with aiofiles.open(this.path + '\\src\\forme.txt', 'r') as infile:
			async for line in infile:
				line = re.sub('[:,]', '', line.rstrip())
				listFormes.append(line.split(' '))

		# POKEMON TABLE
		dexNumber = 1
		async with aiofiles.open(this.path + '\\src\\species.txt', 'r') as infile:
			async for line in infile:
				# Use a bisect to create a range of indexes based on the species' generation
				sortedDict = sorted(dictIndex.keys())
				insertion = bisect.bisect_left(sortedDict, dexNumber)

				# Offset if needed
				if insertion == len(sortedDict) or sortedDict[insertion] != dexNumber:
					 insertion -= 1

				# Get the list and copy to itself so that it doesn't modify the dictionary
				data = dictIndex[sortedDict[insertion]]
				data = data[:]

				# Append the species' name
				line = line.rstrip()
				data.append(line)

				# Add attributes
				if line in listMega:
					data.append(1)
				else:
					data.append(0)

				if line in listAlolan:
					data.append(1)
				else:
					data.append(0)

				if line in listGalarian:
					data.append(1)
				else:
					data.append(0)

				if line in listGmax:
					data.append(1)
				else:
					data.append(0)

				# Pad for formes
				data.append(None)

				await this.cursor.execute("INSERT INTO pokemon(dex_limit, region, gen, species, mega, alolan, galarian, gmax, forme) VALUES (?,?,?,?,?,?,?,?,?)", data)
				dexNumber += 1

		# Add species formes
		async with aiofiles.open(this.path + '\\src\\forme.txt', 'r') as infile:
			async for line in infile:
				line = re.sub('[:,]', '', line.rstrip())
				split = line.split(' ')

				# Find the species' row
				await this.cursor.execute("SELECT * FROM pokemon WHERE species LIKE ?", (split[0],))
				result = list(await this.cursor.fetchone())
				del split[0]

				# Add the forme to the row
				joined = ', '.join(split)
				await this.cursor.execute("UPDATE pokemon SET forme = ? WHERE dex = ?", (joined, result[0]))

		await this.db.commit()

	async def __populatePokedex(this):
		# POKEDEX TABLE
		# Grabbed the data from
		# https://github.com/veekun/pokedex/blob/master/pokedex/data/csv/pokemon_species_flavor_text.csv

		# Oh boy this is a thick lad
		async with aiofiles.open(this.path + '\\src\\pokedex.json', mode = 'r', encoding = 'utf-8') as infile:
			bigFile = json.loads(await infile.read())
			for key in bigFile:
				text = re.sub(r'[\n\f]', ' ', key['flavor_text'])
				data = [key['species_id'], key['version_id'],key['language_id'], text]

				await this.cursor.execute("INSERT INTO pokedex (species, version, language, text) VALUES (?,?,?,?)", data)

		await this.db.commit()

	async def getPokemon(this, value):
		# Search based on species name
		if isinstance(value, str):
			await this.cursor.execute('SELECT * FROM pokemon WHERE species LIKE ?', (value,))

		# Search based on dex number
		elif isinstance(value, int):
			await this.cursor.execute('SELECT * FROM pokemon WHERE dex LIKE ?', (str(value),))

		return await this.cursor.fetchone()

	async def getPokedex(this, value, version, language = 9):
		if isinstance(value, str):
			await this.cursor.execute('SELECT * FROM pokemon WHERE species LIKE ?', (value,))

			# Get the species' dex number
			info = await this.cursor.fetchone()
			info = list(info)
			value = info[0]
			version = info[2]

		# 9 = English language
		await this.cursor.execute('SELECT * FROM pokedex WHERE species LIKE ? AND version LIKE ? AND language LIKE ?', (value, version, language))
		result = await this.cursor.fetchone()
		result = list(result)

		# Return the flavor text
		return result[4]