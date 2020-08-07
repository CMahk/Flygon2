import aiohttp
import asyncio
from bot.flygon import Flygon2

async def main():
	flygon = Flygon2()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())