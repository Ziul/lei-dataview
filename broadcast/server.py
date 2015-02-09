#!/usr/bin/python
# -*- coding:utf-8 -*-

""" AF_INET  server with broadcast. """

import socket
import select
import signal
import sys
#import subprocess
#import shlex
import logging
import datetime
from threading import Thread

FILE_NAME = './teste.txt'


class Server(Thread):

    """docstring for Server"""

    def __init__(self, ip='127.0.0.1', port=9000, verbose=False, broad=True):
        # Thread.__init__(self)
        super(Server, self).__init__()
        self.port = port
        # self.ip=socket.gethostname()
        self.ip = ip
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients_list = []
        self.verbose = verbose
        self.broad = broad
        self.ret = self.Setup()
        signal.signal(signal.SIGINT, self.signal_handler)
        self.live = False
        self.output = ''
        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.INFO)
        if not self.broad:
            self.file = open(FILE_NAME, 'w')
            self.file.close()

        # create a file handler based on date
        # dt = datetime.datetime.now()
        # name = dt.strftime("%A, %d. %B %Y %I:%M%p")
        # name = dt.strftime("%A, %d. %B %Y")
        # handler = logging.FileHandler('%s.log' % name)

        # define a logging format
        # formatter = logging.Formatter('%(asctime)s - %(message)s')
        # handler.setFormatter(formatter)
        # add the handlers to the logger
        # self.logger.addHandler(handler)

    def Setup(self):
        """ Setup server status and let it ready to be used"""
        self.server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1)
        try:
            self.server_socket.bind((self.ip, self.port))
            self.server_socket.listen(10)
            self.clients_list.append(self.server_socket)
            return (
                "Server seted Up on %s (%s:%s)" % (
                    socket.gethostname(),
                    self.ip,
                    self.port)
            )
        except socket.error as error:
            if str(error) == '[Errno 13] Permission denied':
                self.ret = """
  .-------------------------------.
 ( You need Super Cow Powers here.%s
  '-------------------------------'
         \   ^__^
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||

""" % ' )'.rjust(14)
            else:
                self.ret = """
  .-------------------------------.
 %s
  '-------------------------------'
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||

""" % ('(  ' + str(error) + ' )'.rjust(14))

            raise Exception(self.ret)

    def broadcast(self, sock, message):
        """
        Do not send the message to master socket and the client who has send
        us the message
        """
        # remove any \n on mesage
        # message = message.replace('\n', '')
        # save server message on logging
        # self.logger.info(str(message))
        for mysocket in self.clients_list:
            if mysocket != self.server_socket and mysocket != sock:
                try:
                    # broadcast message
                    mysocket.send(message)

                except:
                    # broken socket connection may be, chat client pressed
                    # ctrl+c for example
                    mysocket.close()
                    if mysocket in self.clients_list:
                        self.clients_list.remove(mysocket)

    def Clients(self):
        """ Returns the list of clients """
        return len(self.clients_list)

    def stop(self):
        self.shutdown()

    def shutdown(self):
        """ Shutdown the server """
        self.live = False
        for sock in self.clients_list:
            try:
                sock.send('Shutting Down server')
            except:
                pass
            sock.close()
            self.clients_list.remove(sock)
        self.server_socket.close()

    def run(self):
        """ Active rotine when server is alive """
        self.live = True
        if self.broad:
            # sys.stdout.write("Socket ready\n")
            self.ret = "Socket ready\n"
            sys.stdout.write(self.ret)
        else:
            sys.stdout.write(
                "File " +
                FILE_NAME +
                " cleaned and ready to be written\n")
        while self.live:
            # Get the list sockets which are ready to be read through select
            try:
                read_sockets, write_sockets, error_sockets = select.select(
                    self.clients_list, [], [], 0.5)
            except socket.error:
                self.signal_handler(0, 0)
                exit(0)
            except select.error:
                self.signal_handler(0, 0)
                exit(0)
            for sock in read_sockets:
                # New connection
                if sock == self.server_socket:
                    # Handle the case in which there is a new connection
                    # recieved through server_socket
                    sockfd, addr = self.server_socket.accept()
                    self.clients_list.append(sockfd)
                    self.ret = "Client (%s: %s) connected" % addr
                    self.ret += " [%d clients]\n" % (
                        len(self.clients_list) - 1)
                    sys.stdout.write(self.ret)
                    # print "Client %s connected" % sockfd
                    # self.broadcast(sockfd, "\n[%s:%s] entered room\n" % addr)

                # Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    try:
                        # In Windows, sometimes when a TCP program closes
                        # abruptly, a "Connection reset by peer" exception will
                        # be thrown
                        data = sock.recv(1024)

                        if data:
                            # self.broadcast(sock,'<' + str(sock.getpeername())
                            # + '> [' + data + ']')
                            self.output = data
                            if self.broad:
                                self.broadcast(sock, data)
                            else:
                                try:
                                    # Somehow, it need a time here
                                    sys.stdout.write(" ")
                                    self.file = open(FILE_NAME, 'a')
                                    self.file.write(data)
                                    self.file.close()
                                except Exception as e:
                                    Exception(
                                        "Fail in open the file: %s" %
                                        str(e))
                            if self.verbose:
                                sys.stdout.write(data)

                    except:
                        # self.broadcast(sock, "Client (%s, %s) is offline"
                        #   % addr)
                        self.ret = "Client (%s, %s) is offline" % addr
                        self.ret += " [%d clients]\n" % (
                            len(self.clients_list) - 1)
                        sys.stdout.write(self.ret)
                        sock.close()
                        if sock in self.clients_list:
                            self.clients_list.remove(sock)
                        continue

    def signal_handler(self, my_signal, frame):
        """ handle the signal interruption """
        print '\rCtrl+C hited!'
        for sock in self.clients_list:
            try:
                sock.send('Shutting Down server')
            except:
                sys.stdout.write('Recived %s from %s' % (my_signal, frame))
            sock.close()
            self.clients_list.remove(sock)
        self.server_socket.close()
        sys.exit()


def main():
    """ Main routine

    Start up a UDP server and broadcast it as default """
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options] [port [baudrate]]",
        description="Server - A simple terminal program for Broadcasting data."
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
                      default=88
                      )

    parser.add_option("-b",
                      dest="broad",
                      action="store_true",
                      help="Enable the broadcast, disabling file write",
                      default=True
                      )

    parser.add_option("-f",
                      dest="broad",
                      action="store_false",
                      help="Enable the file write, disabling the broadcast",
                      default=True
                      )

    (options, args) = parser.parse_args()
    if len(args) == 0:
        sys.stdout.write("Default mode\n")
    if options.quiet is False:
        sys.stdout.write("Quiet mode\n")

    k = Server(
        ip='127.0.0.1',
        port=options.port,
        verbose=options.quiet,
        broad=options.broad)
    print k.ret
    k.run()

if __name__ == '__main__':
    main()
