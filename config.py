import configparser
import os

class Config():
	def __init__(this, configPath):
		# Make a config file if one isn't found
		if not os.path.exists(configPath):
			this.__populateConfig(configPath)

		# Begin parsing through config.ini
		config = configparser.ConfigParser()
		config.read(configPath, encoding = 'utf-8')

		this.online = config.getboolean('GENERAL', 'OnlineMode', fallback = ConfigDefaults.online)
		this.offlinePrompted = config.getboolean('GENERAL', 'OfflinePrompted', fallback = ConfigDefaults.offlinePrompted)
		this.offlinePrompted = config.getboolean('GENERAL', 'OfflineDownloaded', fallback = ConfigDefaults.offlineDownloaded)

		this.token = config.get('DISCORD', 'Token', fallback = ConfigDefaults.token)
		this.commandPrefix = config.get('DISCORD', 'CommandPrefix', fallback = ConfigDefaults.commandPrefix)
		this.limitToChannels = config.getboolean('DISCORD', 'LimitToChannels', fallback = ConfigDefaults.limitToChannels)

		# If only specified channels are being used, grab the channel IDs
		if (this.limitToChannels):
			this.channels = config.get('DISCORD', 'Channels', fallback = ConfigDefaults.channels)

	# Default config
	def __populateConfig(this, configPath):
		with open(configPath, 'a') as infile:
			config = configparser.ConfigParser()
			config.optionxform = str
			config['GENERAL'] = {'OnlineMode': '1', 'OfflinePrompted': '0', 'OfflineDownloaded': '0'}
			config['DISCORD'] = {'Token': '', 'CommandPrefix' : '.', 'LimitToChannels': '0', 'Channels' : ''}
			config.write(infile)

class ConfigDefaults:
	online = True
	offlinePrompted = False
	offlineDownloaded = False

	token = None
	commandPrefix = '.'
	limitToChannels = False
	channels = None