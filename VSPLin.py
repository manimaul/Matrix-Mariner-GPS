#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import pty
import os
import termios
import sys

#default 4800 baud serial port attributes
DEFAULTATTR = [0, 0, 3260, 0, 12, 12, ['\x03', '\x1c', '\x7f', '\x15', '\x01', 0, 0, \
                                       '\x00', '\x11', '\x13', '\x1a', '\x00', '\x12', \
                                       '\x0f', '\x17', '\x16', '\x00', '\x00', '\x00', \
                                       '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                                       '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00']]

class vsp:
    def __init__(self, dir='/tmp/dev', pname='vgps'):
        self.pname = pname #prefix name of virtual com ports
        self.dir = os.path.abspath(dir) #directory where symlinks to virtual serial ports will reside
        self.comlst = [] #list of tuples describing virtual serial ports (dev, name, vcom)
        #dev = int - slave fd to be read from
        #name = string - full path simlinking to slave fd
        #vcom = int - master fd to be written to
        self.bytes = 0
        try:
            os.makedirs(self.dir)
        except OSError:
            pass
        for file in os.listdir(self.dir):
            if file.startswith('vgps'):
                fpath = self.dir + '/' + file
                print 'removing: ', fpath
                os.remove(fpath)
        try: 
            os.makedirs(self.dir, 0777) #create a directory for virtual serial device(s)
        except OSError:
            pass
    
    def findNextCOM(self):
        fls = os.listdir(self.dir)
        n = []
        for f in fls:
            if f.startswith(self.pname):
                n.append(int(f[4:f.__len__()]))
        if len(n) > 0:
            return self.dir + '/' + self.pname + str(max(n)+1)
        else:
            return self.dir + '/' + self.pname +'0'
    
    def createCOM(self, comstr=''): #gpstty is the port to replicate, times is number of ports to spawn
        if comstr == '':
            slave_link = self.findNextCOM()
        else:
            slave_link = comstr
        master_fd, slave_fd = pty.openpty() #spawn device
        termios.tcsetattr(slave_fd, termios.TCSANOW, DEFAULTATTR) #set serial device attributes
        slave_fn = os.ttyname(slave_fd)
        try:
            #slave_link = self.findNextCOM()
            os.symlink(slave_fn, slave_link) #create simlink to device file name
            self.comlst.append((slave_fd, slave_link, master_fd))
            return slave_link
        except OSError:
            os.close(master_fd)
            os.close(slave_fd)
            
    def removeCOM(self, tpl):
        os.remove(tpl[1]) #delete the simlink
        os.close(tpl[0]) #close the slave_fd
        os.close(tpl[2]) #close the master_fd
        self.comlst.remove(tpl)
        
    def write(self, line):
        self.bytes += sys.getsizeof(line)
        if self.bytes >= 256000: #flush every 200KB... approximately 200 lines
            self.flushCOM()
        for com in self.comlst:
            os.write(com[2], line)
    
    def flushCOM(self):
        self.bytes = 0
        for com in self.comlst:
            print 'flushing:', com[1]
            termios.tcflush(com[0], termios.TCIOFLUSH)
        
    def close(self):
        for each in self.comlst:
            self.removeCOM(each)
