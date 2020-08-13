import asyncio
import os
import pathlib
import __main__

class Embed():
	def __init__(this, poke):
		this.__poke = poke

		# Get the current working directory
		cwd = str(pathlib.Path(__main__.__file__).resolve().parent)
		this.__filePath = cwd + '\\sprites' + '\\'

		# Determine which directory to pull from
		this.__filePath += this.__dir(poke.getGen(), poke.isShiny())

		# Get the species' attributes
		foundAttributes = this.__attributes(poke.isMega(), poke.isAlolan(), poke.isGalarian(), poke.isGigantamax())

		# Append everything together (sprites folder > gen +/- shiny folder > species > forme > attribute > .png / .gif)
		this.__filePath += '\\' + poke.getSpecies() + this.__forme(poke.getForme()) + foundAttributes + this.__extension(poke.getGen())

	# Determine which directory to return
	def __dir(this, gen, shiny):
		directory = ''
		if gen >= 6:
			directory = 'ani'
		elif gen == 5:
			directory = 'gen5ani'
		else:
			directory = 'gen' + str(gen)

		# Shinies have their own directory beside the gen
		if (shiny):
			directory += '-shiny'

		return directory

	def __shiny(this, shiny):
		if (shiny):
			return '-shiny'
		else:
			return ''

	def __forme(this, forme):
		if forme != '':
			return '-' + forme
		else:
			return ''

	def __attributes(this, mega, alolan, galarian, gmax):
		if (mega):
			return '-mega'
		elif (alolan):
			return '-alola'
		elif (galarian):
			return '-galar'
		elif (gmax):
			return '-gmax'
		else:
			return ''

	def __extension(this, gen):
		if gen >= 5:
			return '.gif'
		else:
			return '.png'

	def __str__(this):
		return this.__filePath