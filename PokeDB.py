import os.path

# 802 species * 1.3 rounded up to nearest prime number
TABLE_SIZE_SPECIES = 1049

# 46 megas * 1.3 rounded up to nearest prime number
TABLE_SIZE_MEGA = 61

# 18 Alolan forms * 1.3 rounded up to nearest prime number
TABLE_SIZE_ALOLAN = 29

GEN_DICT = {
	"gen1": 151,
	"gen2": 251,
	"gen3": 386,
	"gen4": 493,
	"gen5": 649,
	"gen6": 721,
	"gen7": 802
	}

DESCRIPTORS = ['gen1', 'gen2', 'gen3', 'gen4', 'gen5', 'gen6', 'gen7', 'shiny', 'mega', 'alolan']

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
speciesTable = [[]] * TABLE_SIZE_SPECIES
populateTable('species.txt', speciesTable, TABLE_SIZE_SPECIES)

megasTable = [[]] * TABLE_SIZE_MEGA
populateTable('mega.txt', megasTable, TABLE_SIZE_MEGA)

alolanTable = [[]] * TABLE_SIZE_ALOLAN
populateTable('alolan.txt', alolanTable, TABLE_SIZE_ALOLAN)