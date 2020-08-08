import aiosqlite
import asyncio
import bisect
import re
import os
import json

class pokedb():
	def __init__(this):
		this.path = os.path.abspath(os.path.dirname(__file__))
		this.db = None
		this.cursor = None
		
	def __loadList(this, file):
		fileList = []
		with open(this.path + '\\src\\' + file, 'r') as infile:
			for line in infile:
				line = line.rstrip()
				fileList.append(line)

		return fileList

	async def setup(this):
		# Setup the db schema
		this.db = await aiosqlite.connect(this.path + '\\poke.db')
		this.cursor = await this.db.cursor()
		with open(this.path + '\\schema.sql', 'r') as schema:
			await this.cursor.executescript(schema.read())

		# Setup the db if it isn't already (see if the first row exists)
		await this.cursor.execute('SELECT * FROM pokemon WHERE dex LIKE ?', '1')
		check = await this.cursor.fetchone()
		if check is None:
			await this.__populate()

	async def __populate(this):
		# The list corresponds to: [species total for the generation, default game version, region, generation]
		# See Constants.DICT_VERSION_ID for specifics on what default game version is used to get flavor text
		dictIndex = {
			1: [151, 1, 'kanto', 1],
			152: [251, 6, 'johto', 2],
			252: [386, 9, 'hoenn', 3],
			387: [493, 14, 'sinnoh', 4],
			494: [649, 21, 'unova', 5],
			650: [721, 26, 'kalos', 6],
			722: [809, 29, 'alola', 7],
			#TODO: Flavor text for SwSh
			810: [892, None, 'galar', 8]
			}

		# Load the files into lists
		listMega = this.__loadList('mega.txt')
		listAlolan = this.__loadList('alolan.txt')
		listGalarian = this.__loadList('galarian.txt')
		listGmax = this.__loadList('gmax.txt')

		listFormes = []
		with open(this.path + '\\src\\forme.txt', 'r') as infile:
			for line in infile:
				line = line.rstrip()
				line = re.sub('[:,]', '', line)
				split = line.split(' ')
				listFormes.append(split)

		# POKEMON TABLE
		index = 1
		with open(this.path + '\\src\\species.txt', 'r') as infile:
			for line in infile:
				line = line.rstrip()

				# Use a bisect to create a range of indexes based on the species' generation
				sortedDict = sorted(dictIndex.keys())
				insertion = bisect.bisect_left(sortedDict, index)

				# Offset if needed
				if insertion == len(sortedDict) or sortedDict[insertion] != index:
					 insertion -= 1

				# Get the list and copy to itself so that it doesn't modify the dictionary
				data = dictIndex[sortedDict[insertion]]
				data = data[:]

				# Append the species' name
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

				data.append(None)

				await this.cursor.execute("INSERT INTO pokemon(dex_limit, dex_version, region, gen, species, mega, alolan, galarian, gmax, forme) VALUES (?,?,?,?,?,?,?,?,?,?)", data)
				index += 1

		# Add species formes
		with open(this.path + '\\src\\forme.txt', 'r') as infile:
			for line in infile:
				line = line.rstrip()
				line = re.sub('[:,]', '', line)
				split = line.split(' ')

				await this.cursor.execute("SELECT * FROM pokemon WHERE species LIKE ?", (split[0],))
				result = await this.cursor.fetchone()
				result =  list(result)
				del split[0]
				joined = ', '.join(split)
				await this.cursor.execute("UPDATE pokemon SET forme = ? WHERE dex = ?", (joined, result[0]))

		await this.db.commit()

		# POKEDEX TABLE
		# Grabbed the data from
		# https://github.com/veekun/pokedex/blob/master/pokedex/data/csv/pokemon_species_flavor_text.csv

		# Oh boy this is a thick lad
		with open(this.path + '\\src\\pokedex.json', 'r', encoding = 'utf-8') as infile:
			bigFile = json.load(infile)
			for key in bigFile:
				data = []
				data.append(key['species_id'])
				data.append(key['version_id'])
				data.append(key['language_id'])
				text = key['flavor_text']
				text = re.sub(r'[\n\f]', ' ', text)
				data.append(text)

				await this.cursor.execute("INSERT INTO pokedex (species, version, language, text) VALUES (?,?,?,?)", data)

		await this.db.commit()

	async def getPokemon(this, value):
		# Search based on species name
		if isinstance(value, str):
			await this.cursor.execute('SELECT * FROM pokemon WHERE species LIKE ?', (value,))

		# Search based on dex number
		elif isinstance(value, int):
			await this.cursor.execute('SELECT * FROM pokemon WHERE dex LIKE ?', value)

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