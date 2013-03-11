#!/usr/bin/env python

import sys
if sys.version_info < (2, 5):
    print "Sorry, requires Python 2.5, 2.6 or 2.7."
    sys.exit(1)

import tellstick_api
import json

from bottle import *
from configobj import ConfigObj
from validate import Validator

# Constants
CONFIG_PATH = 'config.ini'
CONFIG_SPEC = 'configspec.ini'

app = Bottle()

# TODO wrap using virtualenv / py2exe
def main():
	config = ConfigObj(CONFIG_PATH, configspec=CONFIG_SPEC)
	validator = Validator()
	result = config.validate(validator, copy=True)

	if result is False:
		print "Config file validation failed"
		sys.exit(1)

	# Write out default values
	config.write()

	tellstick_api.set_config(config)
	app.mount('/json', tellstick_api.app)
	
	debug(config['debug'])
	run(app,
		host = config['host'],
		port = config['port'],
		reloader = config['debug'])

@app.route('/')
def server_static():
	return static_file('index.html', root='.')
	
@app.route('/example.html')
def server_static():
	return static_file('example.html', root='.')

@app.route('/static/<filepath:path>')
def server_static(filepath='index.html'):
	return static_file(filepath, root='./static')

if __name__ == "__main__":
    main()