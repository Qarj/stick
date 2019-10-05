#!/usr/bin/python3
import configparser
import os
import sys
version = "0.1.0"

config = configparser.ConfigParser()

if os.path.exists('stick.ini'):
    config.read('stick.ini')
else:
    config.read('test/test.ini')

dest = config['DEFAULT']['dest']
print (dest)

for section in config.sections():
    source = config[section]['source']
    destination_basename = os.path.basename(source)
    cmd = f"robocopy {source} {dest}\{destination_basename} /MIR /Z /R:2 /W:2 /J"
    print (os.system(cmd))
    print ('---> ' + cmd)