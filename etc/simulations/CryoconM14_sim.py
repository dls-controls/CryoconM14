#!/bin/env python2.4

from pkg_resources import require
require('dls_serial_sim==1.8')
from dls_serial_sim import serial_device
import re, os

class CryoconM14(serial_device):
    Terminator = "\r\n"
#    debug = True
    
    def __init__(self):
        '''Constructor.  Remember to call the base class constructor.'''
        serial_device.__init__(self,
            protocolBranches = ["sensorraw", "temp", "setdate", "date", "settime",\
                                "time", "ipaddress", "macAddress", "reseed"])
        print "Initialising CryoconM14 simulator, V1.0"
        self.raw = dict(zip('ABCD',[1,2,3,4]))
        self.temp = dict(zip('ABCD',[11,12,13,14]))
        self.ipad = '0.0.0.0'
        self.mac = '00:01:02:03:04:05'
        self.date = '01/02/2003'
        self.time = '01:02:03'
        self.seedset = int(False)
        self.on = True
        self.command("diaglevel 5")
        return
        
    def reply(self, command):
        '''This function must be defined. It is called by the serial_sim system
        whenever an asyn command is sent down the line. Must return a string
        with a response to the command or None.'''
        if self.diagnosticLevel() > 4:
            print "Rx: %s"%[command]
        result = None
        if not self.on:
            if self.diagnosticLevel() > 1:
                print "No response as device is off."
            return result

        # Parse the command
        m = command.split()
        if len(m) == 0:
            if self.diagnosticLevel() > 1:
                print "CryoconM14_sim: empty command string"
            return result

        query = command.find('?')
        if query == -1: #So a Put request
            if len(m) == 1: #Reseed averaging filter
                if m[0] == 'SYS:RES':
                    self.seedset = int(True)
                elif self.diagnosticLevel() > 1:
                    print "CryoconM14_sim: no match to Put command: %s"%[command]
            elif len(m) == 2: #Put request for system data
                if m[0] == 'SYS:DATE':
                    self.date = m[1].strip('"')
                elif m[0] == 'SYS:TIME':
                    self.time = m[1].strip('"')
                elif self.diagnosticLevel() > 1:
                    print "CryoconM14_sim: no match to Put command: %s"%[command]
            elif self.diagnosticLevel() > 1:
                print "CryoconM14_sim: no match to Put command: %s"%[command]
        else:
            if len(m) == 1: #Get request for system
                if m[0] == 'SYS:DATE?':
                    result = self.date
                elif m[0] == 'SYS:TIME?':
                    result = self.time
                elif m[0] == 'NETW:IPAD?':
                    result = self.ipad
                elif m[0] ==  'NETW:MAC?':
                    result = self.mac
                elif self.diagnosticLevel() > 1:
                    print "CryoconM14_sim: no match to System Get command: %s"%[command]

            elif len(m) == 2: #Get request for specific sensor
                key = m[1][0]
                if key in self.raw: #Same for self.temp
                    if m[1][2:7] == 'SENPR':
                        result = self.raw[key]
                        print "Returning "+key+":SENPR =",result
                    elif m[1][2:6] == 'TEMP':
                        result = self.temp[key]
                        print "Returning "+key+":TEMP =",result
                    elif self.diagnosticLevel() > 1:
                        print "CryoconM14_sim: no match to Channel Get command: %s"%[command]
            else:
                if self.diagnosticLevel() > 1:
                    print "CryoconM14_sim: too many spaces in Get command: %s"%[command]
        return result

    def getseed(self):
        print "###################CryoconM14_sim: getseed() called."
        return self.seedset
        
    def command(self, text):
        '''Interface function for commands from the test suite.'''
        '''Superceded by RPC calls'''
        print "###################CryoconM14_sim: Received command: %s"%text
        args = text.split()
        if args[0] == "Time":
            self.time = args[1]
        elif args[0] == "Date":
            self.date = args[1]
        elif args[0] == "MAC":
            self.mac = args[1]
        elif args[0] == "IPad":
            self.ipad = args[1]
        elif args[0] == "SetSeedOff":
            self.seedset = False
        elif args[0] == "Seed":
            self.response("Seed",self.seedset)
        elif args[0] == "Raw":
            self.raw[args[1]] = float(args[2])
        elif args[0] == "Temp":
            self.temp[args[1]] = float(args[2])
        elif args[0] == "Off":
            self.On = False
        elif args[0] == "On":
            self.On = True
        else:
            serial_device.command(self, text)

    def initialise(self):
        '''Called by the framework when the power is switched on.'''
        self.on = 1

if __name__ == "__main__":
    # little test function that runs only when you run this file
    dev = CryoconM14()
    dev.start_ip(8001)
    dev.start_debug(9001)
    # do a raw_input() to stop the program exiting immediately
    raw_input()

