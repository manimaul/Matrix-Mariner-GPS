#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

from win32com.client import Dispatch
from scanwin32 import comports
from serial import Serial

class vspe:
    def __init__(self):
        self.vs = Dispatch("VSPE.VSPEApi")
        self.activationKey = 'SRBGMZSYPuIHWILsmLjF5CDyBL3GQYD0IPIEvcZBgPQg8gS9xkGA9CDyBL3GQYD0IPIE' + \
                        'vcZBgPQg8gS9xkGA9CDyBL3GQYD0IPIEvcZBgPQg8gS9xkGA9CDyBL3GQYD0IPIEvcZB' + \
                        'gPQg8gS9xkGA9CDyBL3GQYD0IPIEvcZBgPRJEEYxlJg+4gdYguyYuMXkIPIEvcZBgPQg' + \
                        '8gS9xkGA9CDyBL3GQYD0IPIEvcZBgPQg8gS9xkGA9CDyBL3GQYD0IPIEvcZBgPQg8gS9' + \
                        'xkGA9CDyBL3GQYD0IPIEvcZBgPQg8gS9xkGA9CDyBL3GQYD0IPIEvcZBgPQg8gS9xkGA' + \
                        '9JyUaC2ZWE1DZV2+wYWlRm7FFYrW3MDbZg8MkQsOQ8r1IPIEvcZBgPQg8gS9xkGA9Lzr' + \
                        'hjimHDiMlKqr6pSiw9CDl9n+0bAgFr2ho7nXjCoTMHYzt4tsbEkJGNktLGVG42SZ63Ub' + \
                        'mIUNcKmfhSzXldVCLhfvZv3StR9c/vkYG471Nh62eC1qIYuBUvm+a3BK8iR0POD8w5ov' + \
                        'tuYr0T8aQP3eh4b8lUwnPHG9NRJxerttq/+/zX7c++9LDSQym3ThbWesK+A+X/vNw9qD' + \
                        'gYt1dsJxDEEytsCRiT7bTiV5Djh1RlpIwETXWA089hiE9OYd7GpjKLq5dQOqSVcA3Fg1' + \
                        'Wfdbqn/yn8q0/AIDOd0iZlbVeLY68zKh1Di4gGEoa1kR8EOBp2mxeaFrfwUm3DsJ5Pc0' + \
                        '4f7aEw9XljfBUwl/bAs3LVH5HRii8lXZvUVvnnfpcQ==1F250CF0960AE1C09E9450C8' + \
                        '16DE1232';
    
    def initialize(self):
        self.vs.vspe_activate(self.activationKey)
        self.vs.vspe_initialize()
        self.vs.vspe_destroyAllDevices()
        self.vs.vspe_stopEmulation()
        self.vs.vspe_release()
        self.comlst = [] #com ports already being used
        print 'vspe initialized'    

    def findNextCOM(self):
        next = True
        num = 1
        used = []
        for each in self.comlst:
            used.append(each[1])
        for port in comports(False):
            used.append(port[1])
        while next:
            name = 'COM' + str(num)
            try:
                used.index(name)
                num += 1
            except ValueError:
                next = False
                return num
            if num == 99:
                next = False
                return None
               
    def createCOM(self, comstr=''):
        #comstr must be COM#... ex. COM3 
        if comstr != '':
            num = int(comstr[3:comstr.__len__()])
        else:
            num = self.findNextCOM()
        self.vs.vspe_stopEmulation()
        self.vs.vspe_release()
        self.vs.vspe_initialize()
        # create Connector (COM#, no baud rate emulation)
        com = str(num)+';0' 
        dev = self.vs.vspe_createDevice('Connector',com) #int to be closed by vspe.vspe_destroyDevice
        # start emulation
        self.vs.vspe_startEmulation()
        name = 'COM' + str(num) #name to be opened/closed by serial
        vcom = Serial(name, 38400, timeout=.5)
        tpl = (dev, name, vcom)
        self.comlst.append(tpl)
        return name

    def removeCOM(self, tpl):
        '''tpl = (dev, name, vcom)'''
        tpl[2].close()
        self.vs.vspe_destroyDevice(tpl[0])
        self.comlst.remove(tpl)
        
    def write(self, line):
        for com in self.comlst:
            com[2].write(line)
        
    def close(self):
        for each in self.comlst:
            self.removeCOM(each)
        self.vs.vspe_stopEmulation()
        self.vs.vspe_release()

if __name__ == '__main__':
    myvs = vspe()
    myvs.initialize()
    myvs.createCOM()
    print myvs.comlst
    myvs.createCOM()
    print myvs.comlst
    myvs.close()