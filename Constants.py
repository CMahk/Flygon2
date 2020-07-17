# Error messages
ERROR_GEN = 'Invalid generation given. Please provide a generation between 1 and 7'
ERROR_SHINY = 'Shiny pokemon do not exist in gen 1'
ERROR_SPECIES = 'Invalid species given.'
ERROR_MULTIPLE_SPECIES = 'Multiple species given. Please provide only one species.'
ERROR_NO_SPECIES = 'No species was given.'
ERROR_MEGA = 'This species can not mega evolve.'
ERROR_ALOLAN = 'This species does not have an Alolan forme.'
ERROR_GALARIAN = 'This species does not have a Galarian forme.'
ERROR_GMAX = 'This species can not gigantamax.'
ERROR_MEGA_GEN8 = 'Mega forms are unavailable in gen 8.'
ERROR_MEGA_GMAX = 'Not all given forms can be used together.'
ERROR_FORME = 'This species does not have the specified forme.'
ERROR_ATTRIBUTES = 'Invalid attributes given.'

DICT_GEN = {
	'gen1': 'kanto',
	'gen2': 'johto',
	'gen3': 'hoenn',
	'gen4': 'sinnoh',
	'gen5': 'unova',
	'gen6': 'kalos',
	'gen7': 'alola',
	'gen8': 'galar'
	}

DICT_DEFAULT_VERSION = {
	'gen1': 1,
	'gen2': 6,
	'gen3': 9,
	'gen4': 14,
	'gen5': 21,
	'gen6': 26,
	'gen7': 29
	}

DICT_DEX = {
	'gen1': 151,
	'gen2': 251,
	'gen3': 386,
	'gen4': 493,
	'gen5': 649,
	'gen6': 721,
	'gen7': 809,
	'gen8': 892
	}

# For comparing with DICT_GEN
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
	'ultra-moon': 'alola',
	'sword': 'galar',
	'shield': 'galar'
	}

DICT_LANG = {
	'en': 'english',
	'eng': 'english',
	'fr': 'french',
	'fre': 'french',
	'ge': 'german',
	'ger': 'german',
	'it': 'italian',
	'ita': 'italian',
	'jpn': 'japanese',
	'jp': 'japanese',
	'ko': 'korean',
	'kor': 'korean',
	'de': 'dutch',
	'deu': 'dutch',
	'sp': 'spanish',
	'es': 'spanish'
	}

DICT_VERSION_ID = {
	'red': 1,
	'blue': 2,
	'yellow': 3,
	'gold': 4,
	'silver': 5,
	'crystal': 6,
	'ruby': 7,
	'sapphire': 8,
	'emerald': 9,
	'firered': 10,
	'leafgreen': 11,
	'diamond': 12,
	'pearl': 13,
	'platinum': 14,
	'heartgold': 15,
	'soulsilver': 16,
	'black': 17,
	'white': 18,
	'colosseum': 19,
	'xd': 20,
	'black2': 21,
	'white2': 22,
	'x': 23,
	'y': 24,
	'omegaruby': 25,
	'alphasapphire': 26,
	'sun': 27,
	'moon': 28,
	'ultrasun': 29,
	'ultramoon': 30
	}

DESCRIPTORS = ['gen1', 'gen2', 'gen3', 'gen4', 'gen5', 'gen6', 'gen7', 'shiny', 'mega', 'alolan', 'galarian', 'gmax']
TYPES = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fighting', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'poison', 'psychic', 'rock', 'steel', 'water']

# Directories to grab sprites from
URL_PNG_LIST = ['gen1', 'gen2', 'gen2-shiny', 'gen3', 'gen3-shiny', 'gen4', 'gen4-shiny']
URL_GIF_LIST = ['gen5ani', 'gen5ani-shiny', 'ani', 'ani-shiny']