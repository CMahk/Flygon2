import sys

async def main():
	from bot.constants import Constants
	from bot.flygon import Flygon2
	from config import Config
	from sql.pokedb import PokeDB

	config = Config(Constants.CONFIG_DEFAULT_PATH)

	pokemonDB = PokeDB()
	await pokemonDB.setup()

	flygon = Flygon2(config, pokemonDB)
	await flygon.run()
	await pokemonDB.close()

if __name__ == '__main__':
	if not sys.version_info >= (3, 8):
		print('Python 3.8+ is required. You are running this with version %s' % sys.version.split()[0])
	else:
		import asyncio
		loop = asyncio.get_event_loop()
		loop.run_until_complete(main())
