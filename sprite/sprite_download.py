import aiofiles
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import Constants
import os

PATH = os.path.abspath(os.path.dirname(__file__))

async def main():
	makeFolders(Constants.URL_PNG_LIST)
	makeFolders(Constants.URL_GIF_LIST)

	async with aiohttp.ClientSession() as session:
		for url in Constants.URL_PNG_LIST:
			await findImages(session, url, 'png')

		for url in Constants.URL_GIF_LIST:
			await findImages(session, url, 'gif')

async def findImages(session, url, extension):
	# Grab the webpage to parse through
	async with session.get('https://play.pokemonshowdown.com/sprites/' + url + '/') as resp:
		if resp.status == 200:
			print('Downloading %s %ss...' % (url, extension), end = ' ', flush = True)
			extension = '.' + extension

			# Find hyperlink tags
			soup = BeautifulSoup(await resp.text(), 'html.parser')
			for link in soup.find_all('a'):
				# Ensure that the link has the given extension
				if (link.get('href')[-1 * len(extension):] == extension):

					# If given the OK, write the file locally
					async with session.get('https://play.pokemonshowdown.com/sprites/' + url + '/' + link.get('href')) as fileResp:
						if fileResp.status == 200:
							image = await aiofiles.open(PATH + '\\' + url + '\\' + link.get('href'), mode = 'wb')
							await image.write(await fileResp.read())
							await image.close()

						else:
							print('Error accessing image: %s in %s' % (link.get('href'), url))
			print('Done')

		else:
			print('Error accessing URL: %s' % url)

def makeFolders(list):
	for name in list:
		if not os.path.exists(PATH + '\\' + name):
			os.mkdir(PATH + '\\' + name)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())