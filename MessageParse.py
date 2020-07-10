# Chandler Mahkorn 7/9/20 - 10:34 PM
import re
import os.path

# 802 species * 1.3 rounded up to nearest prime number
TABLE_SIZE_SPECIES = 1049

# 46 megas * 1.3 rounded up to nearest prime number
TABLE_SIZE_MEGAS = 61

GEN_DICT = {
	"gen1": 151,
	"gen2": 251,
	"gen3": 386,
	"gen4": 493,
	"gen5": 649,
	"gen6": 721,
	"gen7": 802
	}

DESCRIPTORS = ['.gen1', '.gen2', '.gen3', '.gen4', '.gen5', '.gen6', '.gen7', 'shiny', 'mega', 'alolan']

class MessageParse():
	def __init__(this, message = ""):
		# Pokedex limits per generation
		this.path = os.path.abspath(os.path.dirname(__file__))

		# Create the hash tables
		this.speciesTable = [[]] * TABLE_SIZE_SPECIES
		this.hashSpecies()

		this.megasTable = [[]] * TABLE_SIZE_MEGAS
		this.hashMegas()

		# Get the generation, then the rest of the list
		this.gen, this.list = this.splitMessage(message)

		this.species = this.getSpecies(this.list)

		# Prep for modifiers
		this.shiny = False
		this.mega = False
		this.getModifiers(this.list)

	def hashSpecies(this):
		# Bernstein hash function
		with open(this.path + '\\species.txt', 'r') as infile:
			for line in infile:
				line = line.rstrip()
				hashVal = 5381
				hashVal *= 33

				lineVal = 0
				for char in line:
					lineVal += ord(char)

				hashVal += lineVal
				hashVal %= TABLE_SIZE_SPECIES

				# Add the species to the list in the table's index
				indexContents = this.speciesTable[hashVal].copy()
				indexContents.append(line)
				this.speciesTable[hashVal] = indexContents

	def hashMegas(this):
		# Bernstein hash function
		with open(this.path + '\\megas.txt', 'r') as infile:
			for line in infile:
				line = line.rstrip()
				hashVal = 5381
				hashVal *= 33

				lineVal = 0
				for char in line:
					lineVal += ord(char)

				hashVal += lineVal
				hashVal %= TABLE_SIZE_MEGAS

				indexContents = this.megasTable[hashVal].copy()
				indexContents.append(line)
				this.megasTable[hashVal] = indexContents

	def splitMessage(this, message):
		message = message.lower()
		regex = re.sub(r'[^\w\s]', '', message)
		split = regex.split()
		gen = split[0]
		del split[0]
		return gen, split

	def getSpecies(this, list):
		# Get just the species' name
		species = [word for word in list if word not in DESCRIPTORS]
		species = species[0]

		# Hash the name and see if it exists
		hashVal = 5381
		hashVal *= 33
		speciesVal = 0
		for char in species:
			speciesVal += ord(char)

		hashVal += speciesVal
		hashVal %= TABLE_SIZE_SPECIES

		# If the species exists, then that is the assigned name
		if (species in this.speciesTable[hashVal]):
			return species
		else:
			return 'Bad'

	def getModifiers(this, list):
		# Get the modifiers
		if (this.gen != 'gen1'):
			if ('shiny' in list):
				this.shiny = True

		# Check for the species name in the megas hash table
		if (this.gen == 'gen6' or this.gen == 'gen7'):
			if ('mega' in list):
				hashVal = 5381
				hashVal *= 33

				speciesVal = 0
				for char in this.species:
					speciesVal += ord(char)

				hashVal += speciesVal
				hashVal %= TABLE_SIZE_MEGAS
				if (this.species in this.megasTable[hashVal]):
					this.mega = True