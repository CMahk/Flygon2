import asyncio
from bot.flygon import Flygon2
from sql.pokedb import pokedb

async def main():
	pokemonDB = pokedb()
	await pokemonDB.setup()

	flygon = Flygon2('..\\config.ini', pokemonDB)
	await flygon.run()
	await pokemonDB.close()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
