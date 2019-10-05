#!/usr/bin/python3
import configparser
import os
import sys
version = "0.1.0"

import win32com.client

def find_drive_letter(driveName):
    wmi = win32com.client.GetObject ("winmgmts:")
    for usb in wmi.InstancesOf ("Win32_USBHub"):
        print (usb.DeviceID)

    # https://stackoverflow.com/questions/33784537/python-get-name-of-a-usb-flash-drive-device-windows
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")

    # 1. Win32_DiskDrive
    colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_DiskDrive WHERE InterfaceType = \"USB\"")
    DiskDrive_DeviceID = colItems[0].DeviceID.replace('\\', '').replace('.', '')
    DiskDrive_Caption = colItems[0].Caption

    print ('DiskDrive DeviceID:', DiskDrive_DeviceID)

    # 2. Win32_DiskDriveToDiskPartition
    colItems = objSWbemServices.ExecQuery("SELECT * from Win32_DiskDriveToDiskPartition")
    for objItem in colItems:
        if DiskDrive_DeviceID in str(objItem.Antecedent):
            DiskPartition_DeviceID = objItem.Dependent.split('=')[1].replace('"', '')

    print ('DiskPartition DeviceID:', DiskPartition_DeviceID)

    # 3. Win32_LogicalDiskToPartition
    colItems = objSWbemServices.ExecQuery("SELECT * from Win32_LogicalDiskToPartition")
    for objItem in colItems:
        if DiskPartition_DeviceID in str(objItem.Antecedent):
            LogicalDisk_DeviceID = objItem.Dependent.split('=')[1].replace('"', '')

    print ('LogicalDisk DeviceID:', LogicalDisk_DeviceID)

    # 4. Win32_LogicalDisk
    colItems = objSWbemServices.ExecQuery("SELECT * from Win32_LogicalDisk WHERE DeviceID=\"" + LogicalDisk_DeviceID + "\"")
    print ('LogicalDisk VolumeName:', colItems[0].VolumeName)
    print ()

    # putting it together
    print (DiskDrive_Caption)
    print (colItems[0].VolumeName, '(' + LogicalDisk_DeviceID + ')')


#
# Main
#

config = configparser.ConfigParser()

if os.path.exists('stick.ini'):
    config.read('stick.ini')
else:
    config.read('test/test.ini')

dest = config['DEFAULT']['dest']

if not os.path.exists(dest):
    print ()
    print ('-------------------------')
    print ('Memory stick not found!!!')
    print ('-------------------------')
    print (f'\nExpected to find: {dest}')
    input ("\nPress Enter...\n")
    exit(1)

missingSources = []

for section in config.sections():
    source = config[section]['source']
    if not os.path.exists(source):
        missingSources.append(source)
        continue

    destinationBasename = os.path.basename(source)
    cmd = f"robocopy {source} {dest}\{destinationBasename} /MIR /Z /R:2 /W:2 /J"
    print (os.system(cmd))
    print ('---> ' + cmd)

if missingSources:
    print ("\nCould not find the following sources:")
    for missing in missingSources:
        print (f'   {missing}')

input ("\nPress Enter to finish...\n")
