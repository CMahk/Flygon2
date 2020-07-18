import Constants
import os
import re
import sqlite3

class PokeError(Exception):
	def __init__(this, problem, error):
		this.problem = 'Error at: ' + str(problem)
		this.error = error

	def __str__(this):
		return this.problem + '\n' + this.error

class PokeOBJ():
	def __init__(this, message = ""):
		# Split the message; get the generation and species
		split = this.__splitMessage(message)

		try:
			this.__gen = this.__setGen(split[0])
			split.remove(this.getGen())

			this.__species, this.__info = this.__setSpecies(split)
			split.remove(this.getSpecies())

			# Prep for attributes; assume False until proven otherwise
			this.__shiny = False
			this.__mega = False
			this.__alolan = False
			this.__galarian = False
			this.__gmax = False
			this.__setAttributes(split)

		# Raise error back to main
		except PokeError as err:
			raise

	# Splits the message up into generation, then species / attributes
	def __splitMessage(this, message):
		return re.sub(r'[^\w\s]', '', message.lower()).split()

	# Determine if the given generation is valid
	def __setGen(this, gen):
		value = gen[-1:]

		# Ensure that the last character is actually a digit
		if (value.isdigit()):
			value = int(value)
			if (value >= 1 and value <= 7):
				return gen

		# Throw an exception if anything is invalid
		raise PokeError(gen, Constants.ERROR_GEN)

	# Determine if the given species is valid
	def __setSpecies(this, userList):
		# Get just the species' name
		species = [word for word in userList if word not in Constants.DESCRIPTORS]

		# Ensure that only one species is given
		if (len(species) == 1):
			species = species[0]
		elif (len(species) < 1):
			raise PokeError(str(species), Constants.ERROR_NO_SPECIES)
		else:
			raise PokeError(str(species), Constants.ERROR_MULTIPLE_SPECIES)

		# Open up the SQL database to find the species
		pokeDB = sqlite3.connect(os.path.abspath(os.path.dirname(__file__)) + '\\Poke.db')
		cursor = pokeDB.cursor()

		cursor.execute('SELECT * FROM pokemon WHERE species LIKE ?', (species,))
		result = cursor.fetchone()
		
		# If nothing was found, raise an exception
		if (result == 'None'):
			raise PokeError(str(species), Constants.ERROR_SPECIES)

		# Turn the tuple into a list; remove the species name
		result = list(result)

		if (result[1] > Constants.DICT_GEN_DEX[this.getGen()]):
			raise PokeError(str(species), Constants.ERROR_SPECIES_GEN)

		# Keep the dex number and gen; convert the rest to bools
		info = [result[0], result[1], result[2]]
		
		for i in range(0, 3):
			del result[0]

		# Convert the ints into booleans for easier checks later on
		for value in result:
			if value is not None:
				info.append(bool(value))
			else:
				info.append(value)

		# If the species exists, then that is the assigned name
		return species, info

	def __setAttributes(this, split):
		# Get the attributes
		if ('shiny' in split):
			this.__shiny = True
			split.remove('shiny')

		# Check if it can mega evolve
		if ('mega' in split and this.__info[3]):
			this.__mega = True
			split.remove('mega')
		else:
			raise PokeError(str(split), Constants.ERROR_MEGA)

		# Check if it can be Alolan
		if ('alolan' in split):
			if (this.__info[4]):
				this.__alolan = True
				split.remove('alolan')
			else:
				raise PokeError(str(split), Constants.ERROR_ALOLAN)

		# Check if it can be Galarian
		if ('galarian' in split):
			if (this.__info[5]):
				this.__galarian = True
				split.remove('galarian')
			else:
				raise PokeError(str(split), Constants.ERROR_GALARIAN)

		# Check if it can G-Max
		if ('gmax' in split):
			if (this.__info[6]):
				this.__gmax = True
				split.remove('gmax')
			else:
				raise PokeError(str(split), Constants.ERROR_GMAX)

		# Check that the species can have the given forms
		if (this.__shiny and this.__gen == 'gen1'):
			raise PokeError(str(split), Constants.ERROR_SHINY)

		elif (this.__mega and this.__gmax):
			raise PokeError(str(split), Constants.ERROR_MEGA_GMAX)

		elif (this.__mega and (this.__gen != 'gen6' and this.__gen != 'gen7')):
				raise PokeError(str(split), Constants.ERROR_MEGA_GEN)

		goodFormes = []
		for item in split:
			if item in this.__info[7]:
				goodFormes.append(item)

	def getGen(this):
		return this.__gen

	def getSpecies(this):
		return this.__species

	def getAttributes(this):
		return this.__shiny, this.__mega, this.__alolan, this.__galarian, this.__gmax

	def getInfo(this):
		return this.__info

	def __str__(this):
		gen = ('Gen: %s\n' % this.getGen())
		species = ('Species: %s\n' % this.getSpecies())
		attributes = ('Attributes:\n  Shiny: %s\n  Mega: %s\n  Alolan: %s\n  Galarian: %s\n  G-Max: %s\n' % this.getAttributes())
		return gen + species + attributes