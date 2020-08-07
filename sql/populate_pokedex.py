import re
import json
import sqlite3

# Grabbed the data from
# https://github.com/veekun/pokedex/blob/master/pokedex/data/csv/pokemon_species_flavor_text.csv

db = sqlite3.connect('poke.db')
c = db.cursor()

c.execute('''CREATE TABLE pokedex
	(
	row INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT COLLATE BINARY,
	species INTEGER NOT NULL COLLATE BINARY,
	version INTEGER NOT NULL COLLATE BINARY,
	language INTEGER NOT NULL COLLATE BINARY,
	text TEXT
	)''')

# Oh boy this is a thick lad
with open('src\\pokedex.json', 'r', encoding = 'utf-8') as infile:
	bigFile = json.load(infile)
	for key in bigFile:
		data = []
		data.append(key['species_id'])
		data.append(key['version_id'])
		data.append(key['language_id'])
		text = key['flavor_text']
		text = re.sub(r'[\n\f]', ' ', text)
		data.append(text)

		c.execute("INSERT INTO pokedex (species, version, language, text) VALUES (?,?,?,?)", data)

db.commit()
db.close()