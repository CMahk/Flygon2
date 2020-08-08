import asyncio
from bot.constants import Constants
from bot.poke import Poke
from bot.poke import PokeError
from config import Config
import os

class Flygon2():
	def __init__(this, configPath = '..\\config.ini', db = None):
		this.__config = Config(configPath)
		this.__db = db

	async def run(this):
		# Get information on the given pokemon
		print('Please enter a command:\n .gen <attributes> <pokemon>\n')

		loop = True
		while(loop):
			userInput = input()
			if (userInput == 'x'):
				break

			try:
				pokemon = Poke(userInput, this.__db)
				await pokemon.setup()

			except PokeError as err:
				print(err)
				found = False

			else:
				found = True

			if (found):
				print(pokemon)
				entry = await this.__db.getPokedex(pokemon.getIndex(), Constants.DICT_DEFAULT_VERSION.get(pokemon.getGen()), 9)
				print(entry)