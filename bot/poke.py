import asyncio
import aiosqlite
import os
import re

class PokeError(Exception):
	def __init__(this, problem, error, extra = ''):
		this.problem = 'Error at: ' + str(problem)
		this.error = error
		this.extra = extra

	def __str__(this):
		return this.problem + '\n' + this.error + '\n' + this.extra

class Poke():
	def __init__(this, message = "", db = None):
		# Split the message; get the generation and species
		this.__message = message
		this.__db = db

	async def setup(this):
		try:
			split = this.__splitMessage(this.__message)
			this.__gen = this.__setGen(split[0])
			split.remove('gen' + str(this.getGen()))

			await this.__setSpecies(split)
			split.remove(this.getSpecies())

			# Leave only the guaranteed safe words in the split list; keep the unsure words separate
			for word in this.__possibleFormes:
				split.remove(word)

			# Prep for attributes; assume False until proven otherwise
			this.__shiny = False
			this.__mega = False
			this.__alolan = False
			this.__galarian = False
			this.__gmax = False
			this.__forme = ''
			this.__setAttributes(split, this.__possibleFormes)

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
				return int(gen[-1:])

		# Throw an exception if anything is invalid
		raise PokeError(gen, PokeConstants.ERROR_GEN)

	# Determine if the given species is valid
	async def __setSpecies(this, userList):
		# Get just the species' name
		species = [word for word in userList if word not in PokeConstants.DESCRIPTORS]

		possibleFormes = []
		foundSpecies = 0
		theSpecies = None

		# Search the words in the list to see if any are pokemon
		for word in species:
			result = await this.__db.getPokemon(word)
			if result is not None:
				foundSpecies += 1
				theSpecies = result
			else:
				possibleFormes.append(word)
		
		# If nothing was found, or more than one species is found, raise an exception
		if foundSpecies == 0:
			raise PokeError(str(species), PokeConstants.ERROR_SPECIES)
		elif foundSpecies != 1:
			raise PokeError(str(species), PokeConstants.ERROR_MULTIPLE_SPECIES)

		result = list(theSpecies)

		# If the species is not available in the given gen, throw an error
		if (result[3] > this.getGen()):
			raise PokeError(str(species), PokeConstants.ERROR_SPECIES_GEN)

		# Keep the dex number, gen, and species; convert the rest to bools
		info = [result[0], result[3], result[4]]
		species = result[4]
		
		# Get rid of everything but the attributes
		for i in range(0, 5):
			del result[0]

		# Convert the ints into booleans for easier checks later on
		for value in result:
			if value is not None and type(value) is not str:
				info.append(bool(value))
			else:
				# Append a list of valid formes for the species
				if type(value) is str:
					info.append(value.split(', '))
				else:
					info.append(value)

		# If the species exists, then that is the assigned name
		this.__species = info[2]
		this.__index = info[0]
		this.__info = info
		this.__possibleFormes = possibleFormes

	def __setAttributes(this, split, possibleFormes):
		# Get the attributes
		if ('shiny' in split):
			this.__shiny = True

		# Check if it can mega evolve
		if ('mega' in split):
			if (this.__info[3]):
				this.__mega = True
			else:
				raise PokeError(str(split), PokeConstants.ERROR_MEGA)

		# Check if it can be Alolan
		if ('alolan' in split):
			if (this.__info[4]):
				this.__alolan = True
			else:
				raise PokeError(str(split), PokeConstants.ERROR_ALOLAN)

		# Check if it can be Galarian
		if ('galarian' in split):
			if (this.__info[5]):
				this.__galarian = True
			else:
				raise PokeError(str(split), PokeConstants.ERROR_GALARIAN)

		# Check if it can G-Max
		if ('gmax' in split):
			if (this.__info[6]):
				this.__gmax = True
			else:
				raise PokeError(str(split), PokeConstants.ERROR_GMAX)

		# Check that the species can have the given forms
		if (this.__shiny and this.__gen == 1):
			raise PokeError(str(split), PokeConstants.ERROR_SHINY)

		elif (this.__mega and this.__gmax):
			raise PokeError(str(split), PokeConstants.ERROR_MEGA_GMAX)

		elif (this.__mega and (this.__gen != 6 and this.__gen != 7)):
			raise PokeError(str(split), PokeConstants.ERROR_MEGA_GEN)

		elif (this.__gmax and this.__gen != 8):
			raise PokeError(str(split), PokeConstants.ERROR_GMAX_GEN)

		# Get the valid formes and prep for checks
		validFormes = this.__info[7]
		goodForme = []
		formeCount = 0

		# Check if the possible formes are valid formes
		if (validFormes is not None and len(possibleFormes) > 0):
			for word in possibleFormes:
				if word in validFormes:
					formeCount += 1
					goodForme.append(word)
				else:
					# If the possible forme is invalid, throw an error
					if (len(validFormes) > 0):
						raise PokeError(str(possibleFormes), PokeConstants.ERROR_MULTIPLE_FORMES, PokeConstants.INFO_FORMES + str(validFormes))
					else:
						raise PokeError(str(possibleFormes), PokeConstants.ERROR_FORME)
			
			# Also throw an error if there's more than one forme
			if formeCount > 1:
				raise PokeError(str(possibleFormes), PokeConstants.ERROR_MULTIPLE_FORMES)
		
			# Otherwise, we're all good
			this.__forme = goodForme[0]


		# If there's valid formes but no formes are given, grab the first one
		elif (validFormes is not None and len(possibleFormes) == 0):
			if validFormes[0] != 'f':
				this.__forme = validFormes[0]

	def getGen(this):
		return this.__gen

	def getSpecies(this):
		return this.__species

	def getIndex(this):
		return this.__index

	def getAttributes(this):
		return this.__shiny, this.__mega, this.__alolan, this.__galarian, this.__gmax, this.__forme

	def getInfo(this):
		return this.__info

	def __str__(this):
		gen = ('Gen: %s\n' % this.getGen())
		species = ('Species: %s\n' % this.getSpecies())
		attributes = ('Attributes:\n  Shiny: %s\n  Mega: %s\n  Alolan: %s\n  Galarian: %s\n  G-Max: %s\n  Forme: %s\n' % this.getAttributes())
		return gen + species + attributes

# Error messages
class PokeConstants:
	ERROR_GEN = 'Invalid generation given. Please provide a generation between 1 and 7'
	ERROR_SHINY = 'Shiny pokemon do not exist in gen 1'
	ERROR_SPECIES = 'Invalid species given.'
	ERROR_SPECIES_GEN = 'This species is not available in this generation.'
	ERROR_MULTIPLE_SPECIES = 'Multiple species given. Please provide only one species.'
	ERROR_NO_SPECIES = 'No species was given.'
	ERROR_MEGA = 'This species can not mega evolve.'
	ERROR_MEGA_GEN = 'Mega evolution is not available in this generation.'
	ERROR_ALOLAN = 'This species does not have an Alolan forme.'
	ERROR_GALARIAN = 'This species does not have a Galarian forme.'
	ERROR_GMAX = 'This species can not gigantamax.'
	ERROR_GMAX_GEN = 'Gigantamaxed pokemon are only available in generation 8.'
	ERROR_MEGA_GMAX = 'Not all given forms can be used together.'
	ERROR_FORME = 'This species does not have the specified forme.'
	ERROR_MULTIPLE_FORMES = 'Multiple formes were given. Only one can be used at a time.'
	ERROR_ATTRIBUTES = 'Invalid attributes given.'

	DESCRIPTORS = ['gen1', 'gen2', 'gen3', 'gen4', 'gen5', 'gen6', 'gen7', 'shiny', 'mega', 'alolan', 'galarian', 'gmax']
	INFO_FORMES = 'The valid formes for this species include:'