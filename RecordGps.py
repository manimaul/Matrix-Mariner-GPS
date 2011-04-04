#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

from sys import getsizeof

class record:
    def __init__(self, path, file):
        print 'opening ' + file + ' for recording'
        self.file = open(path+file, 'wb')
        self.lines = []
        self.bytes = 0
    
    def rxline(self, line):
        self.lines.append(line)
        self.bytes += getsizeof(line)
        if getsizeof(self.lines) > 512:
            self.write()
            
    def getsize(self):
        if self.bytes > 0:
            kb = round((self.bytes/1024)*.778,1) #i don't know why .778 ... seems to average out about right
            return str(kb) + ' KB'
        else:
            return '0 KB'
        
    def write(self):
        buffer = getsizeof(self.lines)
        num = self.lines.__len__()
        if num > 0:
            print str(buffer) + ' bytes and ' + str(num) + ' lines in buffer'
            print 'writing to file'
            self.file.writelines(self.lines)
            self.lines = []
            
    def close(self):
        self.write()
        self.file.close()
        

if __name__ == '__main__':
    import threading
    import Gpscom
    COM = 'COM3'
    BAUD = 4800
    gps = Gpscom.gps(COM, BAUD, .5)
    threading.Timer(120, gps.close).start() #only hold it open for 120 seconds for the sake of example
    
    PATH = 'C:\\Documents and Settings\\User\\appdata\\local\\WinGippy\\recordings\\'
    FILE = 'test.txt'
    rec = record(PATH, FILE)
    while gps.alive.isSet():
        line = gps.rxline()
        rec.rxline(line)
        print line
        print rec.getsize()
    rec.close()
