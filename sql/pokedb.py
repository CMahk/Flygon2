import aiosqlite
import aiofiles
import asyncio
import bisect
import csv
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
		this.db = await aiosqlite.connect(this.path + "\\poke.db")
		this.cursor = await this.db.cursor()
		async with aiofiles.open(this.path + "\\schema.sql", "r") as schema:
			await this.cursor.executescript(await schema.read())

		# Setup the db if it isn't already (see if the first row exists)
		await this.cursor.execute("SELECT * FROM pokemon WHERE dex LIKE ?", "1")
		checkPoke = await this.cursor.fetchone()
		await this.cursor.execute("SELECT * FROM pokedex WHERE species LIKE ?", "1")
		checkDex = await this.cursor.fetchone()

		if checkPoke is None and checkDex is None:
			print("Database not found. Attempting to build one.")

		if checkPoke is None:
			print("Building pokemon table...")
			await this.__populatePokemon()

		if checkDex is None:
			print("Building pokedex table...")
			await this.__populatePokedex()

	async def __loadList(this, file):
		fileList = []
		async with aiofiles.open(this.path + "\\src\\" + file, "r") as infile:
			async for line in infile:
				fileList.append(line.rstrip())

		return fileList

	async def __populatePokemon(this):
		# The list corresponds to: [species total for the generation, default game version, region, generation]
		# See Constants.DICT_VERSION_ID for specifics on what default game version is used to get flavor text
		dictIndex = {
			1: [151, "kanto", 1],
			152: [251, "johto", 2],
			252: [386, "hoenn", 3],
			387: [493, "sinnoh", 4],
			494: [649, "unova", 5],
			650: [721, "kalos", 6],
			722: [809, "alola", 7],
			810: [892, "galar", 8]
			}

		# POKEMON TABLE
		dexNumber = 1
		with open(this.path + "\\src\\poke.csv", "r", encoding = "utf-8") as infile:
			reader = csv.reader(infile, delimiter = ",")
			# Get the header out of the way
			header = next(reader)
			for row in reader:
				# Parse the CSV data
				rowParsed = []
				for item in row:
					# Cast string numbers to ints
					if (str.isdigit(item)):
						rowParsed.append(int(item))
					# Append null if the string is empty
					elif (item == ""):
						rowParsed.append(None)
					# Replace stand-in characters (they exist to not interfere when splitting the row into a list)
					else:
						item = item.replace(";", ",").replace("@", "'").replace("#", '"')
						rowParsed.append(item)

				# Use a bisect to create a range of indexes based on the species' generation
				sortedDict = sorted(dictIndex.keys())
				insertion = bisect.bisect_left(sortedDict, dexNumber)
				# Offset if needed
				if insertion == len(sortedDict) or sortedDict[insertion] != dexNumber:
					 insertion -= 1

				# Get the list and copy to itself so that it doesn't modify the dictionary
				data = dictIndex[sortedDict[insertion]]
				data = data[:]

				# Append the CSV data
				for item in rowParsed:
					data.append(item)

				# Write to the database
				await this.cursor.execute("INSERT INTO pokemon(dex_limit, region, gen, species, mega, alolan, galarian, gmax, forme, type, height, weight) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", data)
				dexNumber += 1

		await this.db.commit()

	async def __populatePokedex(this):
		# POKEDEX TABLE
		# Oh boy this is a thick lad
		with open(this.path + "\\src\\pokedex.csv", mode = "r", encoding = "utf-8") as infile:
			reader = csv.reader(infile, delimiter = ",")
			# Get the header out of the way
			header = next(reader)
			for row in reader:
				rowParsed = []
				for item in row:
					# Cast string numbers to ints
					if (str.isdigit(item)):
						rowParsed.append(int(item))
					else:
						rowParsed.append(item)

				await this.cursor.execute("INSERT INTO pokedex (species, version, language, text) VALUES (?,?,?,?)", row)

		await this.db.commit()

	async def getPokemon(this, value):
		# Search based on species name
		if isinstance(value, str):
			await this.cursor.execute("SELECT * FROM pokemon WHERE species LIKE ?", (value,))

		# Search based on dex number
		elif isinstance(value, int):
			await this.cursor.execute("SELECT * FROM pokemon WHERE dex LIKE ?", (str(value),))

		return await this.cursor.fetchone()

	async def getPokedex(this, value, version, language = 9):
		if isinstance(value, str):
			await this.cursor.execute("SELECT * FROM pokemon WHERE species LIKE ?", (value,))

			# Get the species' dex number
			info = await this.cursor.fetchone()
			info = list(info)
			value = info[0]
			version = info[2]

		# 9 = English language
		await this.cursor.execute("SELECT * FROM pokedex WHERE species LIKE ? AND version LIKE ? AND language LIKE ?", (value, version, language))
		try:
			result = await this.cursor.fetchone()
			result = list(result)

			# Return the flavor text
			return result[4]
		except:
			return ""