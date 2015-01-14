# coding: utf-8

"""
    Arduino module

    A Interface with the hardware
"""
from mock import MagicMock
try:
    # Terminal Class
    from serial.tools.miniterm import Miniterm
    from serial.serialutil import SerialException
except Exception as error:
    try:
        import serial
    except ImportError as error:
        print 'Install Pyserial'
        raise error
    if float(serial.VERSION) < 2.6:
        print 'Upgrade Pyserial'
    # raise error
    Miniterm = MagicMock()


# import device as sensor
import util


class Arduino(Miniterm):

    """docstring for Arduino

    Done with the ideia that all the interface happens
    by UART

    """
    port = 0
    alive = False
    modules = {}

    def __init__(self, tty, baud=9600, parity="O", timeout=5):
        if tty is not None:
            try:
                super(Arduino, self).__init__(tty, baud, 'N',
                                              False, False)
            except SerialException as e:
                print util.ROOT_MESSAGE
                print e
                exit(-1)
            self.serial.setTimeout(1)
        else:
            """FIXME: remove the code bellow in 
            production environment"""
            self.serial = MagicMock()
            self.serial.readline = util.randomstring
            # raise Exception
        self.readline = self.serial.readline
        self.port = tty
        self.enable()

    def __getitem__(self, key):
        """ Return the value of a item """
        try:
            return getattr(self, key).read_data()
        except TypeError:
            return getattr(self, key).read_data('A')
        except IndexError:
            return getattr(self, key).data
        except SerialException:
            if getattr(self, key).data != '':
                return getattr(self, key).data
            else:
                return self.__getitem__(key)
        except Exception, e:
            raise e

    def __setitem__(self, key, item):
        """ Set a value of a item """
        # getattr(self,key).write_data('r',str(item))
        getattr(self, key).write_data(str(item))

    def enable(self):
        """ Method to enable the micro """
        self.alive = True

    def disable(self):
        """ Method to disable the micro """
        self.alive = False
        self.serial.close()

if __name__ == '__main__':

    # list available ports
    print 'Available ports:'
    PORTS_AVAILABLE = util.available_ports()
    try:
        for i in PORTS_AVAILABLE:
            print '>>> %s' % i
        print '---'
    except TypeError, error:
        print "None device connected"
        exit()

    # choose a port
    if len(PORTS_AVAILABLE) == 1:
        Arduino430 = Arduino(PORTS_AVAILABLE[0])
    print 'Ready'

    # make 10 reads from adc
    # print '\nRaw data \n----------'
    # for x in xrange(1, 11):
    #     print x, Arduino430.adc.read_data('t')

    # define a new reading method
    # def thridfirst(item):
    #     """ Rewritng method """
    #     data = Arduino430.serial.readline()
    #     return data.split(',')[:3]

    # print Arduino430['adc']
    # Arduino430.adc.read_data = thridfirst

    # make 10 reads from adc using the new method
    # print '\nProcessed data \n----------'
    # for x in xrange(1, 11):
    #     print x, Arduino430.adc.flush()

    # example of using a active sensor
    # print '\nActive sensor\'s data \n----------'
    # for x in xrange(1, 11):
    #     print x, Arduino430.pwm.write_data('r', 't')

    # new microcontroller interface
    Arduino430.adc = sensor.Direction(Arduino430.serial, 0)
    print '\nADC data \n----------'
    for x in xrange(1, 10):
        print Arduino430['adc']

    Arduino430.guidao = sensor.Direction(Arduino430.serial, 2)
    print '\nGuidão data \n----------'
    for x in xrange(1, 10):
        print Arduino430['guidao']

    Arduino430.freio = sensor.Freio(Arduino430.serial, 3)
    print '\nFreio data \n----------'
    for x in xrange(1, 11):
        print "Writinh %d..." % x,
        Arduino430['freio'] = x
        print Arduino430['freio']

    # teste number larger than 9
    Arduino430.teste = sensor.Direction(Arduino430.serial, 13)
    print '\nTeste data \n----------'
    for x in xrange(1, 10):
        print Arduino430['teste']

    # closes Arduino430 dependecies
    Arduino430.disable()
