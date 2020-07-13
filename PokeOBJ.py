import Constants
import PokeDB
import re

class PokeError(Exception):
	def __init__(this, problem, error):
		this.problem = 'Error at: ' + str(problem)
		this.error = error

	def __str__(this):
		return this.problem + '\n' + this.error

class PokeOBJ():
	def __init__(this, message = ""):
		# Split the message; get the generation and species
		this.__list = this.__splitMessage(message)

		try:
			this.__gen = this.__setGen(this.__list[0])
			this.__species = this.__setSpecies(this.__list)

			# Prep for modifiers; assume False until proven otherwise
			this.__shiny = False
			this.__mega = False
			this.__setModifiers(this.__list)

		# Raise error back to main
		except PokeError as err:
			raise

	# Return the hash of the given key and table
	def __hash(this, data, size):
		hashVal = hash(data)
		hashVal %= size
		return hashVal

	# Splits the message up into generation, then species / modifiers
	def __splitMessage(this, message):
		return re.sub(r'[^\w\s]', '', message.lower()).split()

	# Determine if the given generation is valid
	def __setGen(this, gen):
		value = gen[-1:]

		# Ensure that the last character is actually a digit
		if (value.isdigit()):
			value = int(value)
			if (value >= 1 and value <= 7):
				this.__list.remove(gen)
				return gen

		# Throw an exception if anything is invalid
		raise PokeError(gen, Constants.ERROR_GEN)

	# Determine if the given species is valid
	def __setSpecies(this, list):
		# Get just the species' name
		species = [word for word in list if word not in Constants.DESCRIPTORS]

		# Ensure that only one species is given
		if (len(species) == 1):
			species = species[0]
		elif (len(species) < 1):
			raise PokeError(str(species), Constants.ERROR_NO_SPECIES)
		else:
			raise PokeError(str(species), Constants.ERROR_MULTIPLE_SPECIES)

		speciesHash = this.__hash(species, Constants.TABLE_SIZE_SPECIES)

		# If the species exists, then that is the assigned name
		if (species in PokeDB.speciesTable[speciesHash]):
			this.__list.remove(species)
			return species
		else:
			raise PokeError(str(species), Constants.ERROR_SPECIES)

	def __setModifiers(this, list):
		# Get the modifiers
		if (this.__gen != 'gen1'):
			if ('shiny' in list):
				this.__shiny = True

		# Check for the species name in the megas hash table
		if (this.__gen == 'gen6' or this.__gen == 'gen7'):
			if ('mega' in list):
				hashVal = this.__hash(this.__species, Constants.TABLE_SIZE_MEGA)
				if (this.__species in PokeDB.megasTable[hashVal]):
					this.__mega = True
				else:
					raise PokeError(str(list), Constants.ERROR_MEGA)

	def getGen(this):
		return this.__gen

	def getSpecies(this):
		return this.__species

	def getModifiers(this):
		return this.__shiny, this.__mega

	def __str__(this):
		gen = ('Gen: %s\n' % this.getGen())
		species = ('Species: %s\n' % this.getSpecies())
		modifiers = ('Modifiers:\n  Shiny: %s\n  Mega: %s\n' % this.getModifiers())
		return gen + species + modifiers