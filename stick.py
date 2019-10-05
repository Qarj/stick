#!/usr/bin/python3
import configparser
import os
import sys
version = "0.1.0"

config = configparser.ConfigParser()
config.read('stick.ini')

dest = config['DEFAULT']['dest']
print (dest)

for section in config.sections():
    source = config[section]['source']
    cmd = f"robocopy {source} {dest} /L"
    print (os.system(cmd))