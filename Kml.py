#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from UserSettings import workdir, homedir
from os.path import abspath
from platform import system
if system() == 'Windows':
    from getIPwin import getIPAddress
if system() == 'Linux':
    from getIPlin import getIPAddress

class ThreadedHttpRequestHandler(BaseHTTPRequestHandler):      
    def do_HEAD(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        except:
            print 'HTTP HEAD response not sent'
    def do_GET(self):
        """Respond to a GET request."""
        try:
            self.send_response(200)
            if self.path == '/gps.png':
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(self.iconPng)
            if self.path == '/plugin.html':
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.plugin)
            if self.path == '/gps.kml':
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.gps)
        except:
            print 'HTTP GET response not sent'

class HTTPServer(ThreadingMixIn, HTTPServer):
    pass

class KMLServer:
    def __init__(self, host='', port=58858):
        self.port = port
        self.handler = ThreadedHttpRequestHandler
        #load gps icon into handler memory
        self.iconhref = '/gps.png</href>'
        d = abspath(workdir + '/rc/gps.png')
        f = open(d, 'rb')
        self.handler.iconPng = f.read()
        f.close()
        #load plugin.html into handler memory
        d = abspath(workdir + '/rc/plugin.html')
        f = open(d, 'r')
        self.handler.plugin = f.read()
        f.close()
        #load gps.kml template into self memory
        d = abspath(workdir + '/rc/gps.kml')
        f = open(d, 'r')
        self.gps_template = f.read()
        f.close()
        #push gps.kml into handler memory
        self.updateKML() #self.gps
        
        self.server = HTTPServer((host, port), self.handler)
        server_thread = Thread(target=self.server.serve_forever, name='kmld-thread')
        server_thread.setDaemon(True)
        server_thread.start()
        print "Server loop running in thread:", server_thread.getName()
        
    def updateKML(self, lat = 0, lon = 0, spd = 0, hdg = 0, alt = 0, rng = 3000, tlt = 30):
        self.handler.gps = self.gps_template %(spd,self.iconhref,lon,lat,rng,tlt,hdg,lon,lat,alt)
        
    def createDesktopKML(self):
        d = abspath(workdir + '/rc/MMG.kml')
        readfile = open(d, 'r')
        data = readfile.read() %(getIPAddress(), str(self.port))
        readfile.close()
        d = abspath(homedir + '/Desktop/MMG.kml')
        writefile = open(d, 'w')
        writefile.writelines(data)
        writefile.close()
        
    def close(self):
        print "Shutting down kml server..."
        self.server.shutdown()
        self.server.server_close()
        print "kml server down"
        
        
if __name__ == '__main__':
    from time import sleep
    myserver = KMLServer()
    while 1:
        sleep(60)
        myserver.close()
        
    