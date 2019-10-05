#!/usr/bin/python3
import configparser
import os
import sys
version = "0.1.0"

config = configparser.ConfigParser()
config.read('stick.ini')

dest = config['DEFAULT']['dest']
print (dest)

for source in config.sections():
    print (config[source]['source'])