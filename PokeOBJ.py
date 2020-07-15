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
		this.__split = this.__splitMessage(message)

		try:
			this.__gen = this.__setGen(this.__split[0])
			this.__species, this.__attributes = this.__setSpecies(this.__split)

			# Prep for attributes; assume False until proven otherwise
			this.__shiny = False
			this.__mega = False
			this.__alolan = False
			this.__galarian = False
			this.__gmax = False
			this.__setAttributes(this.__split, this.__attributes)

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
				this.__split.remove(gen)
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
		del result[0]

		# Convert the ints into booleans for easier checks later on
		boolList = []
		for value in result:
			if (type(value) != str):
				boolList.append(bool(value))
			else:
				boolList.append(value)

		# If the species exists, then that is the assigned name
		this.__split.remove(species)
		return species, boolList

	def __setAttributes(this, split, bools):
		# Get the attributes
		if ('shiny' in split):
			this.__shiny = True

		# Check if it can mega evolve
		if ('mega' in split and bools[0]):
			this.__mega = True
		else:
			raise PokeError(str(split), Constants.ERROR_MEGA)

		# Check if it can be Alolan
		if ('alolan' in split):
			if (bools[1]):
				this.__alolan = True
			else:
				raise PokeError(str(split), Constants.ERROR_ALOLAN)

		if ('galarian' in split):
			if (bools[2]):
				this.__galarian = True
			else:
				raise PokeError(str(split), Constants.ERROR_GALARIAN)

		if ('gmax' in split):
			if (bools[3]):
				this.__gmax = True
			else:
				raise PokeError(str(split), Constants.ERROR_GMAX)

		if (this.__mega and this.__gmax):
			raise PokeError(str(split), Constants.ERROR_MEGA_GMAX)

	def getGen(this):
		return this.__gen

	def getSpecies(this):
		return this.__species

	def getAttributes(this):
		return this.__shiny, this.__mega, this.__alolan, this.__galarian, this.__gmax

	def __str__(this):
		gen = ('Gen: %s\n' % this.getGen())
		species = ('Species: %s\n' % this.getSpecies())
		attributes = ('Attributes:\n  Shiny: %s\n  Mega: %s\n  Alolan: %s\n  Galarian: %s\n  G-Max: %s\n' % this.getAttributes())
		return gen + species + attributes