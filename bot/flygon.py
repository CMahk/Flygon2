import asyncio
from bot.constants import Constants
from bot.embed import Embed
from bot.poke import Poke
from bot.poke import PokeError
import webbrowser

class Flygon2():
	def __init__(this, config = None, db = None):
		this.__config = config
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
				version = Constants.DICT_VERSION_ID.get(this.__config.genDex[pokemon.getGen() - 1])
				entry = await this.__db.getPokedex(pokemon.getDexNumber(), version, 9)
				print(entry)

				embed = Embed(pokemon)
				
				webbrowser.open(str(embed))