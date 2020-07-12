import os
import Constants

# Populate the given table via hashing
def populateTable(fpath, table, size):
	with open(os.path.abspath(os.path.dirname(__file__)) + '\\' + fpath, 'r') as infile:
		# Pull each line and hash it
		for line in infile:
			line = line.rstrip()
			hashVal = hash(line)
			hashVal %= size

			# Add the data to the index's list
			indexContents = table[hashVal].copy()
			indexContents.append(line)
			table[hashVal] = indexContents
		
# Create the hash tables
speciesTable = [[]] * Constants.TABLE_SIZE_SPECIES
populateTable('species.txt', speciesTable, Constants.TABLE_SIZE_SPECIES)

megasTable = [[]] * Constants.TABLE_SIZE_MEGA
populateTable('mega.txt', megasTable, Constants.TABLE_SIZE_MEGA)

alolanTable = [[]] * Constants.TABLE_SIZE_ALOLAN
populateTable('alolan.txt', alolanTable, Constants.TABLE_SIZE_ALOLAN)