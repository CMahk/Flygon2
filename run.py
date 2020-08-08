import aiosqlite
import asyncio
from sql.pokedb import pokedb

async def main():
	myDB = pokedb()
	await myDB.populate()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())