import aiofiles
import configparser
import os

class Config():
	def __init__(this, path):
		this.__path = path
		this.__setup()

	# Default config
	def __setup(this):
		# Make a config file if one isn't found
		if not os.path.exists(this.__path):
			config = configparser.ConfigParser()
			config.optionxform = str

			config['GENERAL'] = {
						'OnlineMode': '1', 
						'OfflinePrompted': '0', 
						'OfflineDownloaded': '0'
						}

			config['DISCORD'] = {
						'Token': '', 
						'CommandPrefix': '.', 
						'LimitToChannels': '0', 
						'Channels': ''
						}

			config['DEFAULTS'] = {
						'Language': 'english',
						'Gen1Dex': 'red', 
						'Gen2Dex': 'crystal', 
						'Gen3Dex': 'emerald', 
						'Gen4Dex': 'platinum', 
						'Gen5Dex': 'black-2', 
						'Gen6Dex': 'y', 
						'Gen7Dex': 'ultra-sun', 
						'Gen8Dex': 'sword'
						}

			with open(this.__path, 'w') as infile:
				config.write(infile)

		# Begin parsing through config.ini
		config = configparser.ConfigParser()
		config.read(this.__path, encoding = 'utf-8')

		this.online = config.getboolean('GENERAL', 'OnlineMode', fallback = ConfigDefaults.online)
		this.offlinePrompted = config.getboolean('GENERAL', 'OfflinePrompted', fallback = ConfigDefaults.offlinePrompted)
		this.offlinePrompted = config.getboolean('GENERAL', 'OfflineDownloaded', fallback = ConfigDefaults.offlineDownloaded)

		this.token = config.get('DISCORD', 'Token', fallback = ConfigDefaults.token)
		this.commandPrefix = config.get('DISCORD', 'CommandPrefix', fallback = ConfigDefaults.commandPrefix)
		this.limitToChannels = config.getboolean('DISCORD', 'LimitToChannels', fallback = ConfigDefaults.limitToChannels)

		# If only specified channels are being used, grab the channel IDs
		if (this.limitToChannels):
			this.channels = config.get('DISCORD', 'Channels', fallback = ConfigDefaults.channels)

		this.genDex = []
		for i in range(1, 9):
			this.genDex.append(config.get('DEFAULTS', 'Gen%iDex' % i, fallback = ConfigDefaults.genDex[i - 1]))

class ConfigDefaults:
	online = True
	offlinePrompted = False
	offlineDownloaded = False

	token = None
	commandPrefix = '.'
	limitToChannels = False
	channels = None

	genDex = ['red', 'crystal', 'emerald', 'platinum', 'black-2', 'y', 'ultra-sun', 'sword']