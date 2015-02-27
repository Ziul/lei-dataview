#!/usr/bin/python
# -*- coding:utf-8 -*-

from dataview import dependencies

if dependencies.check() is False:
    exit()


from dataview.device import Serial_Sensor as Sensor
from dataview.util import check_port
from broadcast.server import Server
from broadcast.client import Client
from datetime import datetime as dt
from time import sleep
import logging
import signal
import threading

# try to keep it equals or more than how many sensors we have
_MAX_PEERS = 2
glove_server = Server()


def signal_handler(signal=0, frame=0):
    global glove_server
    import sys
    sys.stderr.write('\nCtrl+C  pressed!\n\n')
    glove_server.stop()
    sleep(2)
    exit()


def build_logger(name):
    """ Method to build the logger's handler """
    # name = dt.strftime("%A, %d. %B %Y %I:%M%p")
    day = dt.now().strftime("%A, %d. %B %Y - %H:%M")
    from os import path

    root = path.dirname(path.abspath(__file__))
    handler = logging.FileHandler('%s/Logs/%s.log' % (root, day))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # define a logging format
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


def run_sensor(dict_sensor):
    """ Generic action to each sensor """
    name, sensor = dict_sensor
    logger = build_logger(name)

    # define a client from socket
    sensor_stream = Client()
    sleep(0.1)
    sensor.enable()

    print "%s - ready" % name
    while sensor.live:
        if sensor.live:
            # write on server
            data = str(sensor)
            if data != "":
                sensor_stream.write(data + '\n')

                # write on logger
                logger.info(data)
                print data
        else:
            # write on server
            sensor_stream.write("Sensor %s not connected\n" % sensor.address)


def main():
    """ Main method """
    global glove_server
    from os import path, makedirs
    if not path.exists('Logs'):
        makedirs('Logs')

    print "%s" % (dt.now().strftime("%A, %d. %B %Y %I:%M%p"))
    signal.signal(signal.SIGINT, signal_handler)
    sensors_address = {'BioArt & Health': check_port()}
    sensors = {}
    if sensors_address['BioArt & Health'] is None:
        print "None port connected"
        exit()

    glove_server.start()
    for i in sensors_address:
        try:
            sensors[i] = Sensor(sensors_address[i], baudrate=9600, parity='N')
        except Exception, e:
            glove_server.stop()
            sleep(1)
            print e
            exit()

    # result = _pool.map(run_sensor, sensors.items())
    result = threading.Thread(
        target=run_sensor, name='Sensor', args=(sensors.items()))
    result.daemon = False
    result.start()

    # for i in result:
    #     if i:
    #         print "%s not done" % i

    # make sure all clients stoped
    sleep(0.5)
    # stop server
    # glove_server.stop()
    # wait it stop
    glove_server.join()

if __name__ == '__main__':
    main()
