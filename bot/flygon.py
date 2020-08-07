from bot.constants import Constants
from bot.poke import Poke
from bot.poke import PokeError
from config import Config
import os
import sqlite3

class Flygon2():
	def __init__(this, configPath = '..\\config.ini'):
		this.config = Config(configPath)

		# Get information on the given pokemon
		try:
			pokemon = Poke('.gen2 shiny squirtle')
			print(pokemon)

			# Open up the sql database to get the pokedex flavor text
			dbPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..\\sql\\poke.db')
			db = sqlite3.connect(dbPath)
			cursor = db.cursor()
			cursor.execute('SELECT * FROM pokemon WHERE species LIKE ?', (pokemon.getSpecies(),))

			# Get the species' dex number
			speciesDex = list(cursor.fetchone())[0]
			version = Constants.DICT_DEFAULT_VERSION[pokemon.getGen()]

			# 9 = English language
			cursor.execute('SELECT * FROM pokedex WHERE species LIKE ? AND version LIKE ? AND language LIKE ?', (speciesDex, version, 9))
			text = cursor.fetchone()
	
			if text is not None:
				text = list(text)[4]
				print(text)
			else:
				print('No dex entry found for this generation')

		except PokeError as err:
			print(err)