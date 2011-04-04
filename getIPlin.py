#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import socket

def getIPAddressList():
    return [addr for addr in socket.gethostbyname_ex(socket.gethostname())[2]]

def getIPAddress():
    i = '127.0.0.1'
    for addr in getIPAddressList():
        if not addr.startswith("127."):
            i = addr
    return i