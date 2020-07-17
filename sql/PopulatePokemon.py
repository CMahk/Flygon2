import os
import re
import sqlite3

path = os.path.abspath(os.path.dirname(__file__))

db = sqlite3.connect(path + '\\Poke.db')
c = db.cursor()

c.execute('''CREATE TABLE pokemon
	(
	dex INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT COLLATE BINARY,
	gen INTEGER NOT NULL COLLATE BINARY,
	species TEXT NOT NULL,
	mega INTEGER NOT NULL COLLATE BINARY, 
	alolan INTEGER NOT NULL COLLATE BINARY,
	galarian INTEGER NOT NULL COLLATE BINARY,
	gmax INTEGER NOT NULL COLLATE BINARY,
	forme TEXT
	)''')

def loadList(file):
	fileList = []
	with open(path + '\\' + file, 'r') as infile:
		for line in infile:
			line = line.rstrip()
			fileList.append(line)

	return fileList

listMega = loadList('mega.txt')
listAlolan = loadList('alolan.txt')
listGalarian = loadList('galarian.txt')
listGmax = loadList('gmax.txt')

index = 1
with open(path + '\\species.txt', 'r') as infile:
	for line in infile:
		line = line.rstrip()

		data = []

		if (index <= 151):
			data.append(151)

		elif (index <= 251):
			data.append(251)

		elif (index <= 386):
			data.append(386)

		elif (index <= 493):
			data.append(493)

		elif (index <= 649):
			data.append(649)

		elif (index <= 721):
			data.append(721)

		elif (index <= 809):
			data.append(809)

		else:
			data.append(892)

		data.append(line)

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
		c.execute("INSERT INTO pokemon (gen, species, mega, alolan, galarian, gmax) VALUES (?,?,?,?,?,?)", data)
		index += 1

db.commit()

with open(path + '\\forme.txt', 'r') as infile:
	for line in infile:
		line = line.rstrip()
		line = re.sub('[:,]', '', line)
		split = line.split(' ')

		c.execute("SELECT * FROM pokemon WHERE species LIKE ?", (split[0],))
		result = list(c.fetchone())
		del split[0]
		joined = ', '.join(split)
		c.execute("UPDATE pokemon SET forme = ? WHERE dex = ?", (joined, result[0]))

db.commit()
db.close()
