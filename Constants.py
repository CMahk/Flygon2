# 802 species * 1.3 rounded up to nearest prime number
TABLE_SIZE_SPECIES = 1049

# 46 megas * 1.3 rounded up to nearest prime number
TABLE_SIZE_MEGA = 61

# 18 Alolan forms * 1.3 rounded up to nearest prime number
TABLE_SIZE_ALOLAN = 29

# Error messages
ERROR_GEN = 'Invalid generation given. Please provide a generation between 1 and 7'
ERROR_SPECIES = 'Invalid species given.'
ERROR_MULTIPLE_SPECIES = 'Multiple species given. Please provide only one species.'
ERROR_NO_SPECIES = 'No species was given.'
ERROR_MEGA = 'This species can not mega evolve.'
ERROR_MODIFIERS = 'Invalid modifiers given.'

DICT_GEN = {
	'gen1': 'kanto',
	'gen2': 'johto',
	'gen3': 'hoenn',
	'gen4': 'sinnoh',
	'gen5': 'unova',
	'gen6': 'kalos',
	'gen7': 'alola'
	}

DICT_DEX = {
	'gen1': 151,
	'gen2': 251,
	'gen3': 386,
	'gen4': 493,
	'gen5': 649,
	'gen6': 721,
	'gen7': 802
	}

DICT_VERSION = {
	'red': 'kanto',
	'blue': 'kanto',
	'yellow': 'kanto',
	'gold': 'johto',
	'silver': 'johto',
	'crystal': 'johto',
	'ruby': 'hoenn',
	'sapphire': 'hoenn',
	'emerald': 'hoenn',
	'firered': 'kanto',
	'leafgreen': 'kanto',
	'diamond': 'sinnoh',
	'pearl': 'sinnoh',
	'platinum': 'sinnoh',
	'heartgold': 'johto',
	'soulsilver': 'johto',
	'black': 'unova',
	'white': 'unova',
	'black-2': 'unova',
	'white-2': 'unova',
	'x': 'kalos',
	'y': 'kalos',
	'omega-ruby': 'hoenn',
	'alpha-sapphire': 'hoenn',
	'sun': 'alola',
	'moon': 'alola',
	'ultra-sun': 'alola',
	'ultra-moon': 'alola'
	}


DESCRIPTORS = ['gen1', 'gen2', 'gen3', 'gen4', 'gen5', 'gen6', 'gen7', 'shiny', 'mega', 'alolan']
TYPES = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fighting', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'poison', 'psychic', 'rock', 'steel', 'water']

URL_PNG_LIST = ['gen1', 'gen2', 'gen2-shiny', 'gen3', 'gen3-shiny', 'gen4']
URL_GIF_LIST = ['gen5ani', 'gen5ani-shiny', 'ani', 'ani-shiny']