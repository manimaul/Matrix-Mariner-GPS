#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) someone who posted this on the net somewhere... thanks

def getIPAddresses():
    from ctypes import Structure, windll, sizeof
    from ctypes import POINTER, byref
    from ctypes import c_ulong, c_uint, c_ubyte, c_char
    MAX_ADAPTER_DESCRIPTION_LENGTH = 128
    MAX_ADAPTER_NAME_LENGTH = 256
    MAX_ADAPTER_ADDRESS_LENGTH = 8
    class IP_ADDR_STRING(Structure):
        pass
    LP_IP_ADDR_STRING = POINTER(IP_ADDR_STRING)
    IP_ADDR_STRING._fields_ = [
        ("next", LP_IP_ADDR_STRING),
        ("ipAddress", c_char * 16),
        ("ipMask", c_char * 16),
        ("context", c_ulong)]
    class IP_ADAPTER_INFO (Structure):
        pass
    LP_IP_ADAPTER_INFO = POINTER(IP_ADAPTER_INFO)
    IP_ADAPTER_INFO._fields_ = [
        ("next", LP_IP_ADAPTER_INFO),
        ("comboIndex", c_ulong),
        ("adapterName", c_char * (MAX_ADAPTER_NAME_LENGTH + 4)),
        ("description", c_char * (MAX_ADAPTER_DESCRIPTION_LENGTH + 4)),
        ("addressLength", c_uint),
        ("address", c_ubyte * MAX_ADAPTER_ADDRESS_LENGTH),
        ("index", c_ulong),
        ("type", c_uint),
        ("dhcpEnabled", c_uint),
        ("currentIpAddress", LP_IP_ADDR_STRING),
        ("ipAddressList", IP_ADDR_STRING),
        ("gatewayList", IP_ADDR_STRING),
        ("dhcpServer", IP_ADDR_STRING),
        ("haveWins", c_uint),
        ("primaryWinsServer", IP_ADDR_STRING),
        ("secondaryWinsServer", IP_ADDR_STRING),
        ("leaseObtained", c_ulong),
        ("leaseExpires", c_ulong)]
    GetAdaptersInfo = windll.iphlpapi.GetAdaptersInfo
    GetAdaptersInfo.restype = c_ulong
    GetAdaptersInfo.argtypes = [LP_IP_ADAPTER_INFO, POINTER(c_ulong)]
    adapterList = (IP_ADAPTER_INFO * 10)()
    buflen = c_ulong(sizeof(adapterList))
    rc = GetAdaptersInfo(byref(adapterList[0]), byref(buflen))
    if rc == 0:
        for a in adapterList:
            adNode = a.ipAddressList
            while True:
                ipAddr = adNode.ipAddress
                if ipAddr:
                    yield ipAddr
                adNode = adNode.next
                if not adNode:
                    break

def getIPAddress():
    ip = '127.0.0.1'              
    for addr in getIPAddresses():
        if addr != '0.0.0.0':
            ip = addr
    return ip
        
def getIPAddressList():
    iplst = ['127.0.0.1']
    for addr in getIPAddresses():
        if addr != '0.0.0.0':
            iplst.append(addr)
    return iplst

if __name__ == '__main__':
    print getIPAddress()