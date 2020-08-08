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
		try:
			pokemon = Poke('.gen7 shiny gmax venusaur', this.__db)
			await pokemon.setup()

		except PokeError as err:
			print(err)
			found = False

		else:
			found = True

		if (found):
			print(pokemon)
			entry = await this.__db.getPokedex(pokemon.getIndex(), 1, 9)
			print(entry)