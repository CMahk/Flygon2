# Chandler Mahkorn 7/10/20 - 10:52 PM
from PokeDB import *
import re

class PokeOBJ():
	def __init__(this, message = ""):
		# Split the message; get the generation and species
		this.__list = this.__splitMessage(message)

		this.__gen = this.__setGen(this.__list[0])
		this.__species = this.__setSpecies(this.__list)

		# Prep for modifiers; assume False until proven otherwise
		this.__shiny = False
		this.__mega = False
		this.__setModifiers(this.__list)

	# Return the hash of the given key and table
	def __hash(this, data, size):
		hashVal = hash(data)
		hashVal %= size
		return hashVal

	# Splits the message up into generation, then species / modifiers
	def __splitMessage(this, message):
		message = message.lower()
		regex = re.sub(r'[^\w\s]', '', message)
		split = regex.split()
		return split

	# Determine if the given generation is valid
	def __setGen(this, gen):
		value = int(gen[-1:])

		if (value >= 1 and value <= 7):
			return gen
		else:
			return 'None'

	# Determine if the given species is valid
	def __setSpecies(this, list):
		# Get just the species' name
		species = [word for word in list if word not in DESCRIPTORS]

		if (len(species) != 1):
			return 'None'
		else:
			species = species[0]

		speciesHash = this.__hash(species, TABLE_SIZE_SPECIES)

		# If the species exists, then that is the assigned name
		if (species in speciesTable[speciesHash]):
			return species
		else:
			return 'None'

	def __setModifiers(this, list):
		# Get the modifiers
		if (this.__gen != 'gen1'):
			if ('shiny' in list):
				this.__shiny = True

		# Check for the species name in the megas hash table
		if (this.__gen == 'gen6' or this.__gen == 'gen7'):
			if ('mega' in list):
				hashVal = this.__hash(this.__species, TABLE_SIZE_MEGA)
				if (this.__species in megasTable[hashVal]):
					this.__mega = True

	def getGen(this):
		return this.__gen

	def getSpecies(this):
		return this.__species

	def getModifiers(this):
		return this.__shiny, this.__mega