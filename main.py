# Chandler Mahkorn 7/12/20 - 1:27 PM
import aiohttp
import asyncio
import PokeOBJ

try:
	testObj = PokeOBJ.PokeOBJ(".gen7 shiny charizard mega")
	print(testObj)

except PokeOBJ.PokeError as err:
	print(err)