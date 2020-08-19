import asyncio
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

		# Raise error back to main
		except PokeError as err:
			raise

	# Splits the message up into generation, then species / attributes
	def __splitMessage(this, message):
		return re.sub(r"[^\-\w\s]", '', message.lower()).split()

	# Determine if the given generation is valid
	def __setGen(this, gen):
		value = gen[-1:]

		# Ensure that the last character is actually a digit
		if (value.isdigit()):
			value = int(value)
			if (value >= 1 and value <= 8):
				return int(gen[-1:])

		# Throw an exception if anything is invalid
		raise PokeError(gen, PokeConstants.ERROR_GEN)

	# Determine if the given species is valid
	async def __setSpecies(this, split):
		# Get just the species' name
		species = [word for word in split if word not in PokeConstants.DESCRIPTORS]

		# Search the words in the list to see if any are pokemon
		foundSpecies = 0
		theSpecies = None
		possibleFormes = []

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
			raise PokeError(str(species), PokeConstants.ERROR_SPECIES_GEN, PokeConstants.INFO_SPECIES_GEN % result[3])

		# Convert the ints into booleans for easier checks later on
		attributes = []
		for value in result[5:10]:
			if value is not None and type(value) is not str:
				attributes.append(bool(value))
			else:
				# Append a list of valid formes for the species
				if type(value) is str:
					attributes.append(value.split(', '))
				else:
					attributes.append(value)

		# If the species exists, then that is the assigned name
		this.__species = result[4]
		this.__dexNumber = result[0]

		split.remove(this.getSpecies())
		this.__setAttributes(split, attributes, possibleFormes)

	def __setAttributes(this, split, attributes, possibleFormes):
		# Prep for attributes; assume False until proven otherwise
		this.__shiny = False
		this.__mega = False
		this.__alolan = False
		this.__galarian = False
		this.__gmax = False
		this.__forme = ''

		# Get the attributes
		if ('shiny' in split):
			this.__shiny = True

		# Check if it can mega evolve
		if ('mega' in split):
			if (attributes[0]):
				this.__mega = True
			else:
				raise PokeError(str(split), PokeConstants.ERROR_MEGA)

		# Check if it can be Alolan
		if ('alolan' in split):
			if (attributes[1]):
				this.__alolan = True
			else:
				raise PokeError(str(split), PokeConstants.ERROR_ALOLAN)

		# Check if it can be Galarian
		if ('galarian' in split):
			if (attributes[2]):
				this.__galarian = True
			else:
				raise PokeError(str(split), PokeConstants.ERROR_GALAR)

		# Check if it can Gigantamax
		if ('gmax' in split or 'gigantamax' in split):
			if (attributes[3]):
				this.__gmax = True
			else:
				raise PokeError(str(split), PokeConstants.ERROR_GMAX)

		# Check for any discrepencies
		this.__checkLegal(split)

		# Get the valid formes and prep for checks
		validFormes = attributes[4]
		this.__forme = ''
		formeCount = 0

		# Check if the possible formes are valid formes
		if (validFormes is not None and len(possibleFormes) > 0):
			for word in possibleFormes:
				if word in validFormes:
					formeCount += 1
					this.__forme = word
				else:
					# If the possible forme is invalid, throw an error
					if (len(validFormes) > 0):
						raise PokeError(str(possibleFormes), PokeConstants.ERROR_FORME, PokeConstants.INFO_FORMES % validFormes)
		
		# If no formes are available for the species but one is given, throw an error
		elif (validFormes is None and len(possibleFormes) > 0):
			raise PokeError(str(possibleFormes), PokeConstants.ERROR_FORME)

		# Check for edge cases
		this.__speciesEdges(possibleFormes)

		# If there's valid formes but no formes are given, grab the first one
		if (validFormes is not None and this.__forme == ''):
			# Make sure the species can't mega evolve
			if (not attributes[0]):
				if validFormes[0] != 'f':
					this.__forme = validFormes[0]

		# If a forme is given but it's only available in mega forme, throw an error (Charizard, Mewtwo)
		if (attributes[0] and this.__forme != '' and not this.__mega):
			raise PokeError(this.__forme, PokeConstants.ERROR_MEGA_EXCLUSIVE)
					
		# If it's and there's multiple mega formes, grab the first valid one (Charizard, Mewtwo)
		elif (attributes[0] and this.__forme == '' and this.__mega):
			if (attributes[4] is not None and validFormes[0] != 'f'):
				this.__forme = validFormes[0]

	# Edge cases
	def __speciesEdges(this, possibleFormes):
		dexNumber = this.getDexNumber()

		# TODO: Pikachu edge case
		if (dexNumber == 25):
			pass

		# Alcremie edge case
		elif (dexNumber == 869):
			alcremieBase = ['strawberry', 'berry', 'clover', 'flower', 'love', 'ribbon', 'star']
			alcremieSwirl = ['caramel-swirl', 'lemon-cream', 'matcha-cream', 'mint-cream', 'rainbow-swirl', 'ruby-cream', 'ruby-swirl', 'salted-cream', 'vanilla-cream']
				
			# Default base and swirl
			base = 'strawberry'
			swirl = 'vanilla-cream'
			count = 0

			for word in possibleFormes:
				if word in alcremieBase:
					base = word
					count += 1

				elif word in alcremieSwirl:
					swirl = word
					count += 1

			if (count > 2):
				raise PokeError(str(possibleFormes), PokeConstants.ERROR_ALCREMIE_MULTIPLE)
			else:
				this.__forme = swirl + '-' + base

	def __checkLegal(this, split):
		# Check that the species can have the given forms
		if (this.__shiny and this.__gen == 1):
			raise PokeError(str(split), PokeConstants.ERROR_SHINY)

		elif (this.__mega and this.__gmax):
			raise PokeError(str(split), PokeConstants.ERROR_MEGA_GMAX)

		elif (this.__mega and (this.__gen != 6 and this.__gen != 7)):
			raise PokeError(str(split), PokeConstants.ERROR_MEGA_GEN)

		elif (this.__gmax and this.__gen != 8):
			raise PokeError(str(split), PokeConstants.ERROR_GMAX_GEN)

		elif (this.__galarian and this.__gen != 8):
			raise PokeError(str(split), PokeConstants.ERROR_GALAR_GEN)

	def getGen(this):
		return this.__gen

	def getSpecies(this):
		return this.__species

	def getDexNumber(this):
		return this.__dexNumber

	def getForme(this):
		return this.__forme

	def isShiny(this):
		return bool(this.__shiny)

	def isMega(this):
		return bool(this.__mega)

	def isAlolan(this):
		return bool(this.__alolan)

	def isGalarian(this):
		return bool(this.__galarian)

	def isGigantamax(this):
		return bool(this.__gmax)

	def getAttributes(this):
		return this.isShiny(), this.isMega(), this.isAlolan(), this.isGalarian(), this.isGigantamax(), this.getForme()

	def __str__(this):
		gen = ('Gen: %s\n' % this.getGen())
		species = ('Species: %s\n' % this.getSpecies())
		attributes = ('Attributes:\n  Shiny: %s\n  Mega: %s\n  Alolan: %s\n  Galarian: %s\n  G-Max: %s\n  Forme: %s\n' % this.getAttributes())
		return gen + species + attributes

# Error messages
class PokeConstants:
	ERROR_ALCREMIE_MULTIPLE = 'Multiple swirls or bases were given. Only one base and/or one swirl at a time.'
	ERROR_ALOLAN = 'This species does not have an Alolan forme.'
	ERROR_ATTRIBUTES = 'Invalid attributes given.'
	ERROR_FORME = 'This species does not have the specified forme.'
	ERROR_GALAR = 'This species does not have a Galarian forme.'
	ERROR_GALAR_GEN = 'Galarian pokemon are only available in generation 8.'
	ERROR_GEN = 'Invalid generation given. Please provide a generation between 1 and 7'
	ERROR_GMAX = 'This species can not gigantamax.'
	ERROR_GMAX_GEN = 'Gigantamaxed pokemon are only available in generation 8.'
	ERROR_MEGA = 'This species can not mega evolve.'
	ERROR_MEGA_EXCLUSIVE = 'This forme is exclusive to mega evolution.'
	ERROR_MEGA_GEN = 'Mega evolution is not available in this generation.'
	ERROR_MEGA_GMAX = 'Not all given forms can be used together.'
	ERROR_MULTIPLE_FORMES = 'Multiple formes were given. Only one can be used at a time.'
	ERROR_MULTIPLE_SPECIES = 'Multiple species given. Please provide only one species.'
	ERROR_NO_SPECIES = 'No species was given.'
	ERROR_SHINY = 'Shiny pokemon do not exist in gen 1'
	ERROR_SPECIES = 'Invalid species given.'
	ERROR_SPECIES_GEN = 'This species is not available in this generation.'

	DESCRIPTORS = ['gen1', 'gen2', 'gen3', 'gen4', 'gen5', 'gen6', 'gen7', 'shiny', 'mega', 'alolan', 'galarian', 'gmax']
	INFO_FORMES = 'The valid formes for this species include: %s'
	INFO_SPECIES_GEN = 'It can be found in generation %i and above.'