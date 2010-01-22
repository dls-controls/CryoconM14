#!/dls_sw/tools/bin/python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *
#from autotestframework import *

################################################
# Test suite for the CryoconM14 filter wheel
    
class CryoconM14TestSuite(TestSuite):
    def createTests(self):
        # Define the targets for this test suite
        Target("simulation", self,
            iocDirectory="iocs/example_sim",
            iocBootCmd="bin/linux-x86/stexample.sh",
#            iocBootCmd="screen -D -m -L bin/linux-x86/stexample.sh",
            runIocInScreenUnderHudson=True,
            epicsDbFiles="db/example_expanded.db",
#            simulationCmds=['python2.4 data/CryoconM14_sim.py'],
            simDevices=[SimDevice("tmon1", 9001,rpc=True)],
            environment=[('EPICS_CA_REPEATER_PORT','6065'),
                ('EPICS_CA_SERVER_PORT','6064')],
            guiCmds=['edm -x -eolc -m"tmon=SIM-TS-TMON-01,device=SIM-TS-TEMP-01,record1=T1,record2=T2,record3=T3,record4=T4"\
                    data/CryoconM14.edl'])
        Target("hardware", self,
            iocDirectory="iocs/example",
            iocBootCmd="bin/linux-x86/stexample.sh",
#            iocBootCmd="screen -D -m -L bin/linux-x86/stexample.sh",
            epicsDbFiles="db/example_expanded.db",
            guiCmds=['edm -x -eolc -m"tmon=SIM-TS-TMON-01,device=SIM-TS-TEMP-01,record1=T1,record2=T2,record3=T3,record4=T4"\
                    data/CryoconM14.edl'])

        # The tests
        CaseGetMac(self)
        CaseGetIPad(self)
        CaseSetDate(self)
        CaseSetTime(self)
        CaseReseed(self)
        CaseGetRaws(self)
        CaseGetTemps(self)
        CasePowerOffOn(self)
        
################################################
# Intermediate test case class that provides some utility functions
# for this suite

class CryoconM14Case(TestCase):
    def Dummy(self, sensor):
        ''' Dummy to satisfy standard class hierarchy
        '''
        result = 0
        
################################################
# Test cases
    
# Read the MAC Address 
class CaseGetMac(CryoconM14Case):
    def runTest(self):
        '''Retrieve the MAC address.'''
        if self.simulationDevicePresent("tmon1"):
            mac = "00:50:C2:6F:40:33"
            self.simulation("tmon1").mac=mac
            self.putPv("SIM-TS-TMON-01:MAC.PROC",1)
            self.verifyPv("SIM-TS-TMON-01:MAC", mac)
        else:
            self.diagnostic("No Device", 0)
        self.diagnostic("Finished Test", 0)

# Read the IP Address
class CaseGetIPad(CryoconM14Case):
    def runTest(self):
        '''Retrieve the IP address.'''
        if self.simulationDevicePresent("tmon1"):
            ip = "173.23.234.52"
            self.simulation("tmon1").ipad=ip
            self.putPv("SIM-TS-TMON-01:IPAD.PROC",1)
            self.verifyPv("SIM-TS-TMON-01:IPAD", ip)

# Set and get the date
class CaseSetDate(CryoconM14Case):
    def runTest(self):
        '''Set and Get the date.'''
        if self.simulationDevicePresent("tmon1"):
            date = "09/09/2009"
            self.putPv("SIM-TS-TMON-01:SET:DATE", date)
            self.verifyPv("SIM-TS-TMON-01:DATE", date)

# Set and get the time
class CaseSetTime(CryoconM14Case):
    def runTest(self):
        '''Set and Get the time.'''
        if self.simulationDevicePresent("tmon1"):
            time = "14:15:16"
            self.putPv("SIM-TS-TMON-01:SET:TIME", time)
            self.verifyPv("SIM-TS-TMON-01:TIME", time)

# Reseed the averaging filter
class CaseReseed(CryoconM14Case):
    def runTest(self):
        '''Send command to reseed the averaging filter.'''
        if self.simulationDevicePresent("tmon1"):
            sim = self.simulation("tmon1")
            sim.seedset = int(False)
            self.putPv("SIM-TS-TMON-01:RESEED.TPRO", 1)
            self.putPv("SIM-TS-TMON-01:RESEED.PROC", 1)
            seed = sim.seedset
#            seed = self.simulation("tmon1").getseed()
            print 'SEED =',seed
            self.verify(seed, int(True))

# Fix then read all the raw inputs
class CaseGetRaws(CryoconM14Case):
    def runTest(self):
        '''Get the raw channel inputs.'''
        if self.simulationDevicePresent("tmon1"):
            sim = self.simulation("tmon1")
            ports = ['A','B','C','D']
            raws = [50.0,51.0,52.0,53.0]
            for port,raw in zip(ports,raws):
                sim.raw[port]=raw
            self.sleep(15) #Allow time for records to process
            for port,raw in zip(ports,raws):
                self.verifyPv("SIM-TS-TMON-01:%s:RAW"%port, raw)

# Fix then read all the temperatures
class CaseGetTemps(CryoconM14Case):
    def runTest(self):
        '''Get the temperature channel values.'''
        if self.simulationDevicePresent("tmon1"):
            sim = self.simulation("tmon1")
            ports = ['A','B','C','D']
            ids = [1,2,3,4]
            temps = [100.0,101.0,102.0,103.0]
            for port, temp in zip(ports, temps):
                sim.temp[port]=temp
            self.sleep(15) #Allow time for records to process
            for id, temp in zip(ids, temps):
                self.verifyPv("SIM-TS-TEMP-01:T%d" %id, temp)

# Check if database struggles when device is off.
class CasePowerOffOn(CryoconM14Case):
    def runTest(self):
        '''Turn the device off and back on.'''
        if self.simulationDevicePresent("tmon1"):
            sim = self.simulation("tmon1")
            time = "20:21:22"
            sim.on=False #May affect any following tests if this fails.
            try:
                self.putPv("SIM-TS-TMON-01:SET:TIME", time)
                self.verifyPv("SIM-TS-TMON-01:TIME", time)
            except:
                sim.on=True
                self.putPv("SIM-TS-TMON-01:SET:TIME", time)
                self.verifyPv("SIM-TS-TMON-01:TIME", time)

################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    CryoconM14TestSuite()

    
