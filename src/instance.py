#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import os
from tempfile import gettempdir
from UserSettings import opsys

class singleInst():
    def __init__(self):
        self.lockfile = os.path.normpath(gettempdir() + '/' + 'mmgps.lock')
        print self.lockfile
        self.single = True
        if opsys == 'Windows':
            try:
                if(os.path.exists(self.lockfile)): #try to remove lock file
                    os.unlink(self.lockfile)
                os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
            except:
                print 'mmgps is already running'
                self.single = False
        else: # Linux & Mac
            import fcntl
            self.fd = open(self.lockfile, 'w')
            try:
                fcntl.lockf(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                print 'mmgps is already running'
                self.single = False

if __name__=='__main__':
    from time import sleep
    lock = singleInst()
    if lock.single:
        print 'single instance... running'
        sleep(30)
    else:
        print 'another instance is running... quitting'