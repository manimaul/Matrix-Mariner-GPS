#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

from threading import Thread
from SocketServer import TCPServer, ThreadingMixIn, BaseRequestHandler

class ThreadedTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        try:
            self.request.send(self.line)
        except:
            print 'TCP request handle not sent'

class TCPServer(ThreadingMixIn, TCPServer):
    pass

class TCPd:
    def __init__(self, host='127.0.0.1', port=9889):
        if host == 'Any':
            host = ''
        self.handler = ThreadedTCPRequestHandler
        self.server = TCPServer((host, port), self.handler)
        self.handler.line = '$\r\n'
        server_thread = Thread(target=self.server.serve_forever, name='tcpd-thread')
        server_thread.setDaemon(True)
        server_thread.start()
        print "Server loop running in thread:", server_thread.getName()
        
    def serveline(self, line):
        self.handler.line = line
        
    def close(self):
        self.server.shutdown()
        self.server.server_close()
        
if __name__ == '__main__':
    mytcpd = TCPd()
