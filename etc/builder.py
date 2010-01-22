from iocbuilder import Substitution
from iocbuilder.arginfo import *
from iocbuilder.modules.streamDevice import AutoProtocol

class M14_system(Substitution, AutoProtocol):
    '''System wide features of the Cryocon M14 Temperature Monitor'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, tmon, port):
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        tmon   = Simple('EPICS device name for whole unit', str),
        port   = Simple('Serial port identifier', str))

    # Substitution attributes
    TemplateFile = 'M14_system.template'
    Arguments = ArgInfo.Names()

    # AutoProtocol attributes
    ProtocolFiles = ['M14.protocol']


class M14_sensor(Substitution, AutoProtocol):
    '''Cryocon M14 Temperature Monitor individual sensor details. There are 4 channels.'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, record, tmon, sensor, port, scan, device, egu, adel, hihi, high, low, lolo, name = '', desc = '', gda = True):
        # If gda then define gda_name and gda_desc
        if gda:
            gda_name, gda_desc = name, desc
        else:
            gda_name, gda_desc = '', ''
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        record = Simple('Record specifier part of PV name (e.g. T1)', str),
        tmon   = Simple('EPICS device name for whole unit', str),
        sensor = Simple('Index of single sensor (A/B/C/D)', str),
        port   = Simple('Serial port identifier', str),
        scan   = Simple('Scan period', str),
        device = Simple('EPICS device name for single temperature reading', str),
        egu    = Simple('EGU', str),
        adel   = Simple('ADEL', str),
        hihi   = Simple('HIHI', str),
        high   = Simple('HIGH', str),
        low    = Simple('LOW', str),
        lolo   = Simple('LOLO', str),
        name   = Simple('Object name, also used for gda_name if gda', str),
        desc   = Simple('Object description, also used for gda_desc if gda', str),
        gda    = Simple('Set to True to make available to gda', bool))

    # Substitution attributes
    TemplateFile = 'M14_sensor.template'
    Arguments = ArgInfo.Names()

    # AutoProtocol attributes
    ProtocolFiles = ['M14.protocol']


