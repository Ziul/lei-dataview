#!/usr/bin/env python
# coding: utf-8

try:
    from serial.tools.miniterm import Miniterm, CONVERT_CR, CONVERT_CRLF, CONVERT_LF, EXITCHARCTER, MENUCHARACTER
    from serial.tools.list_ports import comports
except Exception as e:
    if float(serial.VERSION) < 2.6:
        print 'Upgrade Pyserial'
    raise e
try:
    from glob import glob
except Exception as e:
    print 'Install glob'
    raise e

from data import DataRead

ROOT_MESSAGE = """
  .-------------------------------.
 ( You need Super Cow Powers here. )
  '-------------------------------'
         \   ^__^
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||

"""


class I2C_Sensor(object):

    """Basic definitions of a sensor"""

    address = 0x00
    port = 0
    mode = 0
    values = []
    live = False

    def __init__(self, port, address, mode=0):
        """ Method to initialize the sensor """
        self.address = address
        self.port = port
        self.mode = mode

        try:
            from smbus import SMBus
            self.bus = SMBus(self.port)
        except IOError:
            self.bus = None
            self.live = False
        except ImportError:
            print "smbus not installed"
        except Exception as e:
            raise e

    def enable(self):
        """ Method to enable the sensor """

        # if aready got a bus for it
        if self.bus:
            self.live = True

    def disable(self):
        """ Method to desable the sensor """
        self.live = False

    def acquire(self, cmd=0):
        """ Method to acquire the values from sensor """
        if self.live:
            return self.bus.read_i2c_block_data(self.address, cmd)

    def __str__(self):
        if self.bus:
            self.acquire()
            return (
                "Sensor at i2c-%d: 0x%x - %s" % (
                    self.port, self.address, self.values)
            )
        else:
            return "Sensor not ready"


class Serial_Sensor(Miniterm):

    def __init__(
            self,
            port,
            baudrate=9600,
            parity='N',
            rtscts=False,
            xonxoff=False,
            echo=False,
            convert_outgoing=CONVERT_CRLF,
            mode=0):
        super(
            Serial_Sensor,
            self).__init__(port,
                           baudrate,
                           parity,
                           rtscts,
                           xonxoff,
                           echo=False,
                           convert_outgoing=CONVERT_CRLF,
                           repr_mode=mode)
        self.serial.timeout = 0

    def enable(self):
        """ Method to enable the sensor """
        self.live = True

    def disable(self, signal=None, frame=None):
        """ Method to desable the sensor """
        self.live = False
        self.serial.close()

    def acquire(self):
        """ Method to acquire the values from sensor """
        if self.live:
            data = ''
            line = ''
            while (line != '\n'):
                line = self.serial.readline()
                data += line
            # if len(data) > 1:
            #     print data,
            #     print '------'
            return str(data)

    def read(self):
        return self.acquire()

    def __str__(self):
        return self.acquire()


if __name__ == '__main__':
    available = []
    available += glob('/dev/ttyUSB*') + glob('/dev/ttyACM*')
    try:
        for port, desc, hwid in sorted(comports()):
            if port not in port:
                available.append(port)
    except Exception as e:
        raise e
    print available
