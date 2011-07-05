#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import os
import ConfigParser
from platform import machine, system

opsys = system()
arch = machine()

workdir = os.getcwd()
homedir = os.path.expanduser('~') #C:\Users\will in win7

if opsys == 'Windows':
    #recrdir = (homedir + '\\appdata\\local\\mmg\\recordings\\')
    #cfgfile = (homedir + '\\appdata\\local\\mmg\\config.txt')
    recrdir = ('C:\\ProgramData\\mmg\\recordings\\')
    cfgdir = ('C:\\ProgramData\\mmg\\')
    cfgfile = ('C:\\ProgramData\\mmg\\config.txt')
    mrecdir = workdir + '\\rc\\recordings\\'
if opsys == 'Linux':
    recrdir = (homedir + '/.mmg/recordings/')
    cfgdir = (homedir + '.mmg/')
    cfgfile = (homedir + '/.mmg/config.txt')
    mrecdir = workdir + '/rc/recordings/'
version = '1.0beta4'
termsAgreed = False

#Input
gpsCOM = ''
gpsBaud = 4800
loopReplays = False
replaySpeed = 1

#Output
vsps = []
tcpip = ''
tcpport = 0
kml = False

#Information
gpstime = True
gpstime_fmt = '24H:M'
timezone = 'Local - from OS'
gpsdate = True
gpsdate_fmt = 'Month, DD YYYY'
latitude = True
longitude = True
llu_fmt = 'DMS' #DMS DMM or DDD
sog = True
sog_fmt = 'KTS' #KTS, MPH or KPH
cog = True
altitude = True
alt_fmt = 'METERS' #METERS or FEET
hdop = True

#Appearance
bgcolor = (0, 0, 0) #black background
colormode = 'Day'
daycolor = (255, 159, 64)
nightcolor = (155, 0, 0)
fontface = 'LCDDotMatrix5x8'
smfontface = 'smallfonts'
mdfontsz = 23
mddefsz = 23 #default size for reset, does not change
smfontsz = 8
smdefsz = 8 #default size for reset, does not change
screenposition = (0, 0)

#KML Variables
kmlrange = '3000'
kmlheading = '0'
kmltilt = '30'

def readcfg():
    #print 'reading config'    
    if os.path.isfile(cfgfile) == True:
        config = ConfigParser.RawConfigParser()
        config.read(cfgfile)
        try:
            ##global
            v = config.get('WinGippy', 'version')
            if v != version:
                print 'config from different version'
                writecfg()
            global termsAgreed
            termsAgreed = config.get('WinGippy', 'termsAgreed')
            
            ##input
            global gpsCOM
            gpsCOM = config.get('Input', 'gpsCOM')
            global gpsBaud
            gpsBaud = config.get('Input', 'gpsBaud')
            global replaySpeed
            replaySpeed = config.getint('Input', 'replaySpeed')
            global loopReplays
            loopReplays = config.getboolean('Input', 'loopReplays')
            
            ##output
            global vsps
            str = config.get('Output', 'vsps')
            vsps = str[2:-2].split('\', \'')
            if vsps == ['']:
                vsps = []
            global tcpip
            tcpip = config.get('Output', 'tcpip')
            global tcpport
            tcpport = config.getint('Output', 'tcpport')
            global kml
            kml = config.getboolean('Output', 'kml')
            
            ##information
            global gpstime
            gpstime = config.getboolean('Information', 'gpstime')
            global gpsdate
            gpsdate = config.getboolean('Information', 'gpsdate')
            global gpsdate_fmt
            gpsdate_fmt = config.get('Information', 'gpsdate_fmt')
            global latitude
            latitude = config.getboolean('Information', 'latitude')
            global longitude
            longitude = config.getboolean('Information', 'longitude')
            global llu_fmt
            llu_fmt = config.get('Information', 'llu_fmt')
            global sog
            sog = config.getboolean('Information', 'sog')
            global sog_fmt
            sog_fmt = config.get('Information', 'sog_fmt')
            global cog
            cog = config.getboolean('Information', 'cog')
            global altitude
            altitude = config.getboolean('Information', 'altitude')
            global alt_fmt
            alt_fmt = config.get('Information', 'alt_fmt')
            global gpstime_fmt
            gpstime_fmt = config.get('Information', 'gpstime_fmt')
            global timezone
            timezone = config.get('Information', 'timezone')
            global hdop
            hdop = config.getboolean('Information', 'hdop')
            ##appearance
            global screenposition
            x = config.getint('Appearance', 'screenx')
            y = config.getint('Appearance', 'screeny')
            screenposition = (x, y)
            global fontface
            fontface = config.get('Appearance', 'fontface')
            global mdfontsz
            mdfontsz = config.getint('Appearance', 'mdfontsz')
            #smfontsz is controlled by mdfontsz
            global daycolor
            daycolor = config.get('Appearance', 'daycolor')
            daycolor = tuple(int(s) for s in daycolor[1:-1].split(','))
            global nightcolor
            nightcolor = config.get('Appearance', 'nightcolor')
            nightcolor = tuple(int(s) for s in nightcolor[1:-1].split(','))
        except:
            print 'resetting config file to defaults'
            writecfg()
    else:
        try: 
            os.makedirs(homedir + '\\appdata\\local\\WinGippy\\')
            writecfg()
        except: pass

def writecfg():
    print 'writing config'
    config = ConfigParser.RawConfigParser()
    
    config.add_section('WinGippy')
    config.set('WinGippy', 'version', version)
    config.set('WinGippy', 'termsAgreed', termsAgreed)
    
    config.add_section('Input')
    config.set('Input', 'gpsCOM', gpsCOM)
    config.set('Input', 'gpsBaud', gpsBaud)
    config.set('Input', 'replaySpeed', replaySpeed)
    config.set('Input', 'loopReplays', loopReplays)
    
    config.add_section('Output')
    config.set('Output', 'vsps', vsps)
    config.set('Output', 'tcpip', tcpip)
    config.set('Output', 'tcpport', tcpport)
    config.set('Output', 'kml', kml)
    
    config.add_section('Information')
    config.set('Information', 'gpstime', gpstime)
    config.set('Information', 'gpsdate', gpsdate)
    config.set('Information', 'gpsdate_fmt', gpsdate_fmt)
    config.set('Information', 'latitude', latitude)
    config.set('Information', 'longitude', longitude)
    config.set('Information', 'llu_fmt', llu_fmt)
    config.set('Information', 'sog', sog)
    config.set('Information', 'sog_fmt', sog_fmt)
    config.set('Information', 'cog', cog)
    config.set('Information', 'altitude', altitude)
    config.set('Information', 'alt_fmt', alt_fmt)
    config.set('Information', 'gpstime_fmt', gpstime_fmt)
    config.set('Information', 'timezone', timezone)
    config.set('Information', 'hdop', hdop)
    
    config.add_section('Appearance')
    config.set('Appearance', 'screenx', screenposition[0])
    config.set('Appearance', 'screeny', screenposition[1])
    config.set('Appearance', 'mdfontsz', mdfontsz)
    config.set('Appearance', 'fontface', fontface)
    config.set('Appearance', 'daycolor', daycolor)
    config.set('Appearance', 'nightcolor', nightcolor)
    
    configfile = open(cfgfile, 'wb')
    config.write(configfile)
    configfile.close()