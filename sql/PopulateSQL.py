import os
import sqlite3

path = os.path.abspath(os.path.dirname(__file__))

db = sqlite3.connect(path + '\\Poke.db')
c = db.cursor()

c.execute('''CREATE TABLE pokemon 
	(
	dex INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT COLLATE BINARY,
	species TEXT NOT NULL UNIQUE,
	mega INTEGER NOT NULL COLLATE BINARY, 
	alolan INTEGER NOT NULL COLLATE BINARY,
	galarian INTEGER NOT NULL COLLATE BINARY,
	gmax INTEGER NOT NULL COLLATE BINARY,
	forme TEXT
	)''')

listSpecies = []
listMega = []
listAlolan = []
listGmax = []
listGalarian = []

with open(path + '\\mega.txt', 'r') as infile:
	for line in infile:
		line = line.rstrip()
		listMega.append(line)

with open(path + '\\alolan.txt', 'r') as infile:
	for line in infile:
		line = line.rstrip()
		listAlolan.append(line)

with open(path + '\\gmax.txt', 'r') as infile:
	for line in infile:
		line = line.rstrip()
		listGmax.append(line)

with open(path + '\\galarian.txt', 'r') as infile:
	for line in infile:
		line = line.rstrip()
		listGalarian.append(line)

with open(path + '\\species.txt', 'r') as infile:
	for line in infile:
		line = line.rstrip()

		data = [line]

		if line in listMega:
			data.append(1)
		else:
			data.append(0)

		if line in listAlolan:
			data.append(1)
		else:
			data.append(0)

		if line in listGalarian:
			data.append(1)
		else:
			data.append(0)

		if line in listGmax:
			data.append(1)
		else:
			data.append(0)

		print(str(data))
		c.execute("INSERT INTO pokemon (species, mega, alolan, galarian, gmax) VALUES (?,?,?,?,?)", data)

db.commit()
db.close()