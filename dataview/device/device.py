#!/usr/bin/env python
# coding: utf-8

"""
    Device module

    Define the basic classes and rotines to a sensor
"""

from startx import BREAK_MSP, DIRECTION_MSP, VELOCITY_MSP, ALL_VALUES
from time import sleep


class Device(object):

    """docstring for Device"""

    type = ''
    name = 'base'
    data = '-----'
    live = False

    def __init__(self, terminal):
        super(Device, self).__init__()
        self.serial = terminal
        self.enable()
        self.flush()

    def enable(self):
        """ Enable the sensor """

        self.live = True

    def desable(self):
        """ Desable the sensor """

        self.live = False

    def flush(self):
        """ Read data """
        try:
            return self.serial.readline()
        except SerialException:
            sleep(0.01)
            return self.flush()


class Active(Device):

    """docstring for Passive"""

    def __init__(self, terminal):
        super(Active, self).__init__(terminal)
        self.data = self.serial.readline()
        self.data = self.data.split('\n')[0]

    def write_data(self, data):
        """ Return actual data from device """
        self.serial.write(str(data))

    def read_data(self, command):
        return None  # self.serial.readline()


class Passive(Device):

    """docstring for Active"""

    def __init__(self, terminal):
        super(Passive, self).__init__(terminal)
        self.data = self.serial.readline()
        self.data = self.data.split('\n')[0]

    def read_data(self, command):
        """ Send some data to device """
        self.serial.write('A')
        self.data = self.serial.readline()
        return self.data

    def write_data(self, command, data):
        return None


class Break(Active):

    """docstring for Break"""

    def __init__(self, terminal, arg=BREAK_MSP):
        super(Break, self).__init__(terminal)
        self.arg = arg

    def write_data(self, data):
        if data == '':
            data = '0'
        data = int(data)
        if (data >= 0) and (data <= 9):
            super(Break, self).write_data(data)


class Direction(Passive):

    """docstring for Direction"""

    def __init__(self, terminal, arg=DIRECTION_MSP):
        super(Direction, self).__init__(terminal)
        self.arg = arg

    def read_data(self):
        return super(Direction, self).read_data(self.arg)


class Velocity(Passive):

    """docstring for Velocity"""

    def __init__(self, terminal, arg=VELOCITY_MSP):
        super(Velocity, self).__init__(terminal)
        self.arg = arg

    def read_data(self):
        return super(Velocity, self).read_data(self.arg)


class Passives(Passive):

    """docstring for Passives"""

    def __init__(self, terminal, arg=ALL_VALUES):
        super(Passives, self).__init__(terminal)
        self.arg = arg

    def read_data(self):
        print "data lida"
        # return super(Passives, self).read_data(self.arg)
        return super(Passives, self).read_data(self.arg)

if __name__ == '__main__':
    import serial
    from glob import glob
    PORTS_AVAILABLE = glob('/dev/ttyUSB*') + glob('/dev/ttyACM*')
    print PORTS_AVAILABLE
    ser = serial.Serial(PORTS_AVAILABLE[0], 4800)
    act = Active(ser)
    print act.write_data('r', 't')
    passive = Passive(ser)
    print passive.read_data('g')
    ser.close()
