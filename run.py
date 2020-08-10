import asyncio
from bot.constants import Constants
from bot.flygon import Flygon2
from config import Config
from sql.pokedb import PokeDB

async def main():
	config = Config(Constants.CONFIG_DEFAULT_PATH)

	pokemonDB = PokeDB()
	await pokemonDB.setup()

	flygon = Flygon2(config, pokemonDB)
	await flygon.run()
	await pokemonDB.close()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
