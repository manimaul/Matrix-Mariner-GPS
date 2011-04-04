#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Scan for serial ports. Linux specific variant that also includes USB/Serial
adapters.

Part of pySerial (http://pyserial.sf.net)
(C) 2009 <cliechti@gmx.net>
"""

import serial
import glob

def scan():
    """scan for available ports. return a list of device names."""
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')

def basiccomlist():
    lst = []
    for name in scan():
        lst.append(name)
    return lst

if __name__=='__main__':
    print "Found ports:"
    for name in scan():
        print name