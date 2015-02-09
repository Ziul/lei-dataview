#!/usr/bin/python
# -*- coding:utf-8 -*-

""" Client to a AF_INET network."""

import socket
import select
import signal
import sys
import time
#from threading import Thread


class Client(object):

    """ Generic client to a AF_INET network"""

    def __init__(self, ip='127.0.0.1', port=9000, verbose=False):
        super(Client, self).__init__()
        self.port = port
        self.ip = ip
        self.verbose = verbose
        self.live = False
        self.ret = self.SetUp()
        try:
            signal.signal(signal.SIGINT, self.signal_handler)
        except Exception as e:
            pass

    def stop(self):
        self.live = False
        self.client_socket.close()
        sys.stdout.write("Closed\n")

    def run(self):
        self.live = True
        sys.stdout.write("Connected as reader only\n")
        time.sleep(0.1)
        while self.live:
            if(self.verbose):
                sys.stdout.write(self.read() + '\n')
            else:
                self.read()
            time.sleep(0.01)

    def SetUp(self):
        """ Conect client to an network ready"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # now connect to the web server on port 88
            # - the normal http port
            self.client_socket.connect((self.ip, self.port))
            return 'Connected'

        except socket.error as ex:
            return "Error with the socket connection"

    def signal_handler(self, signal, frame):
        """ Wait for a interrupt to shoultdown the client"""
        if(signal):
            print '\nCtrl+C hited! Client closed'
        else:
            # print "\rLooks the server is down\n"
            raise Exception("\rLooks the server is down\n")
            self.client_socket.close()
        self.client_socket.close()
        sys.exit()

    def read(self):
        """ Make a read up 1024 chars """
        try:
            return self.client_socket.recv(4096)
        except socket.error as e:
            self.signal_handler(0, 0)

    def write(self, message, quiet=False):
        """ Write on the network """
        try:
            self.client_socket.send(message)
            if(self.verbose):
                sys.stdout.write(message)
        except socket.error as e:
            self.signal_handler(0, 0)

if __name__ == '__main__':
    import optparse
    sys.stdout.flush()
    parser = optparse.OptionParser(
        usage="%prog [options] [port [baudrate]]",
        description="Client - A simple terminal program for Broadcasting data."
    )

    parser.add_option("-q", "--quiet",
                      dest="quiet",
                      action="store_false",
                      help="suppress non error messages",
                      default=True
                      )
    parser.add_option("-p",
                      dest="port",
                      type='int',
                      help="port, a number or a device name",
                      default=8080
                      )

    parser.add_option("--ip",
                      dest="ip",
                      help="""choose a diferent ip to connect (deprected).
                    Default: %default""",
                      default='127.0.0.1'
                      )

    parser.add_option("-t",
                      dest="delay",
                      type='float',
                      help="""set a personal delay, in seconds, on each
                    messagem send by the socket. Default: %default seconds""",
                      default=0.5
                      )

    parser.add_option("-r",
                      dest="reader",
                      action="store_true",
                      help="set the client to be a reader from the server",
                      default=False
                      )

    parser.add_option("-m",
                      dest="message",
                      help="""set a personal message to be send to server
                 (default: %default)""",
                      default='Hello Network world!'
                      )

    (options, args) = parser.parse_args()
    #k=Client(ip=options.ip, port=options.port ,verbose=options.quiet)
    if(options.ip != '127.0.0.1'):
        sys.stderr.write("you are tring to use a deprected function.\nBye\n")
        exit(0)

    if not options.quiet:
        sys.stdout.write("Quiet mode\n")
        sys.stdout.flush()
    k = Client(port=options.port, verbose=options.quiet)
    sys.stdout.write(k.ret + '\n')
    if options.reader:
        sys.stdout.write("Connected as reader only")
        time.sleep(0.1)
        while True:
            if(options.quiet):
                sys.stdout.write(k.read() + '\n')
            else:
                k.read()
            time.sleep(0.1)
    else:
        while True:
            k.write('\n' + options.message)
            time.sleep(options.delay)
