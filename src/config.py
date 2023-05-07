import configparser

config = configparser.ConfigParser()
config.read('config/config.conf')

port = config['flask']['port']