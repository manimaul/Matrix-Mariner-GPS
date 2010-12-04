#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

from string import atof
from operator import xor
from time import strftime, strptime, gmtime, localtime, sleep
from calendar import timegm
from serial import Serial
from threading import Thread, Event, Timer

class gps():
    '''Opens a serial gps or gps-dump text file, reads and formats GGA, RMC, GSA sentences
       raw data lines are also available as self.data_raw (use for VSPE, TCP and KML)'''
    def __init__(self, com='COM1', baud=4800, timeOut=.5, simloop=False):
        ###Options###
        self.format_latlon = 0
        self.requireChecksum = True
        self.echoLine = False #print each received line
        self.ticktime = 1 #set time speed, needed for simulations
        self.freshtime = 5 #reset data when not received for this amount of time in seconds
        self.debug = False
        self.simloop = simloop
        ###raw data###
        self.data_epochUtc = None
        self.rmcCount = 0
        self.ggaCount = 0
        self.gsaCount = 0
        self.vtgCount = 0
        self.data_sog = None #float from RMC
        self.data_cog = None #float from RMC
        self.data_date = None #string from RMC
        self.data_decl = None #float from RMC
        self.data_status = None #string from RMC
        self.data_altM = None #float from GGA
        self.data_utc = None  #float from RMC, GGA
        self.data_lat = None #float from RMC, GGA
        self.data_long = None #float from RMC, GGA
        self.data_mode = None #string from GSA
        self.data_sats = None #int from GGA, GSA
        self.data_hdop = None #float from GGA, GSA
        self.data_raw = '' #string ALL
        #init
        
        self.alive = Event()
        self.alive.set()
        self.tickT = Thread(target=self.ticktock) #start before trying to open thread
        self.tickT.setDaemon(True)
        self.tickT.start()
        self.freshF = Timer(self.freshtime, self.keepfresh)
        self.freshF.setDaemon(True)
        self.keepfresh()
        if not com.endswith('.txt'):
            self.sim = False
            self.comT = Thread(target=self.readCom)
            self.comT.setDaemon(True)
            try: 
                self.com = Serial(com, baud, timeout=timeOut) #open serial port
                self.comT.start()
            except:
                print com + ' not available!'
                self.close()
        else:
            self.sim = True
            self.comT = Thread(target=self.runsim)
            self.comT.setDaemon(True)
            try:
                self.com = open(com, 'rb')
                self.comT.start()
            except:
                print com + ' cannot be openned!'
                self.close()
            
    def setfreshtime(self, freshtime):
        self.freshF.cancel()
        self.freshtime = freshtime
        self.freshF = Timer(self.freshtime, self.keepfresh)
                
    def runsim(self):
        print 'sim file open... reading'
        lines = self.com.readlines()
        self.com.close()
        #begin calculate lines per second of replay file for replay speed
        linecount = 0
        tstamp1 = 0
        line1 = 0
        tstamp2 = 0
        line2 = -1
        delay = .25 #default seconds per line
        for line in lines: #count lines
            linecount += 1
        print 'total lines in file:', linecount
        for line in lines: #count lines until first time code
            line1 += 1
            if self.sentencID(line) == 'RMC': 
                self.rmc(line)
                tstamp1 = self.data_epochUtc
                self.data_epochUtc = None
                print 'got 1st time-stamp from an RMC, line#:', line1, 'epoch:', tstamp1
                break
        for line in reversed(lines): #count lines backwards to first time code
            line2 += 1
            if self.sentencID(line) == 'RMC':
                line2 = linecount - line2
                self.rmc(line)
                tstamp2 = self.data_epochUtc
                self.data_epochUtc = None
                line2 += 1 #its the next line
                print 'got last time-stamp from an RMC, line#:', line2, 'epoch:', tstamp2
                break
        if tstamp1 != 0 and tstamp2 != 0 and tstamp2-tstamp1 != 0:
            seconds = float(tstamp2 - tstamp1)
            numline = float(line2 - line1)
            delay = round(seconds/numline, 3) / self.ticktime
        print 'setting replay delay to: ' + str(delay)
        self.simread(lines, delay)
                
    def simread(self, lines, delay):
        for line in lines:
            if self.alive.isSet():
                if line.__len__() > 0:
                    self.data_raw = line
                    if self.echoLine:
                        print line
                    if self.requireChecksum:
                        if self.checksum(line):
                            self.sortLine(line)
                    elif self.line_inspect(line):
                        self.sortLine(line)
                sleep(delay)
        if self.alive.isSet() and self.simloop == True:
            print 'looping gps playback'
            self.simread(lines, delay)
        else:
            print 'simulation finished'
            self.alive.clear()
        
    def ticktock(self):
        while self.alive.isSet():
            if self.data_epochUtc is not None:
                self.data_epochUtc += 1
            sleep(self.ticktime)
            
    def readCom(self):
        print 'com port open... reading'
        while self.alive.isSet():
            try:
                line = self.com.readline()
                if line.__len__() > 0:
                    self.data_raw = line
                    if self.echoLine:
                        print line
                    if self.requireChecksum:
                        if self.checksum(line):
                            self.sortLine(line)
                    elif self.line_inspect(line):
                        self.sortLine(line)
            except:
                print 'GPS receiver was disconnected!'
                self.alive.clear()
                          
    def keepfresh(self):
        print 'keeping fresh'
        if self.debug:
            print 'keepfresh: in the last ' + str(self.freshtime) + 'seconds'
            print 'rmc count is', self.rmcCount
            print 'gga count is', self.ggaCount
            print 'gsa count is', self.gsaCount
            print 'vtg count is', self.vtgCount
        if self.rmcCount == 0:
            self.data_date = None #string from RMC
            self.data_decl = None #float from RMC
            self.data_status = None #string from RMC
        if self.rmcCount == 0 and self.vtgCount == 0:
            self.data_sog = None #float from RMC
            self.data_cog = None #float from RMC
        if self.ggaCount == 0:
            self.data_altM = None #float from GGA
        if self.ggaCount == 0 and self.rmcCount == 0:
            self.data_utc = None  #float from RMC, GGA
            self.data_lat = None #float from RMC, GGA
            self.data_long = None #float from RMC, GGA
        if self.gsaCount == 0:
            self.data_mode = None #string from GSA
        if self.gsaCount == 0 and self.ggaCount == 0:
            self.data_sats = None #int from GGA, GSA
            self.data_hdop = None #float from GGA, GSA
        self.rmcCount = 0
        self.ggaCount = 0
        self.gsaCount = 0
        self.vtgCount = 0
        if self.alive.isSet():
            self.freshF = Timer(self.freshtime, self.keepfresh)
            self.freshF.setDaemon(True)
            self.freshF.start()
    
    def rxline(self):
        self.data_rawLast = self.data_raw
        while self.data_rawLast == self.data_raw and self.alive.isSet(): #wait for new line
                sleep(.1)
        self.data_rawLast = self.data_raw  
        return self.data_rawLast
            
    def sortLine(self, line):
        if self.sentencID(line) == 'RMC':
            self.rmc(line)
        if self.sentencID(line) == 'GGA':
            self.gga(line)
        if self.sentencID(line) == 'GSA':
            self.gsa(line)
        if self.sentencID(line) == 'VTG':
            self.vtg(line)
    
    def close(self):
        self.alive.clear()
        if self.comT.isAlive():
            print 'joining Gpscom.comT'
            self.comT.join()
        print 'joining Gpscom.tickT'
        self.tickT.join()
        print 'joining Gpscom.freshT'
        self.freshF.cancel()
        #self.freshT.join()
        if hasattr(self, 'com') and self.sim == False: #simulation files are already closed
            print 'closing Gpscom.com'
            self.com.close()

    def line_inspect(self, line):
        line = str(line)
        len = line.__len__()
        r = False
        if len >= 7:
            if line[0] == '$' and line[-5] == '*' and line[-2:len] == '\r\n':
                r = True
        return r
    
    def sentencID(self, line):
        if line.__len__() > 6:
            return line[3:6]
        
    def checksum(self, line): #see if the sentence has a valid checksum
        try:
            nmea = map(ord, line[1:line.index('*')])
            chksum = reduce(xor, nmea)
            chksum = str(hex(chksum))[2:4]
            chksum = chksum.upper()
            schksum = line.find("*")
            schksum = line[schksum+1:schksum+3]
            if schksum[0] == '0':
                schksum = schksum[1]
            if chksum == schksum:
                return True
            else:
                return False
        except:
            if self.debug == True:
                print 'checksum - GPS sending malformed data:'
                print line
            return False
    
    def fmt_multistatus(self):
        if self.sim == False:
            stat = 'GPS'
        else:
            stat = 'SIM!'
        if self.data_status != None:
            stat += ' ' + self.data_status
        if self.data_mode != None:
            stat += ' ' + self.data_mode
        if self.data_sats != None:
            stat += ' ' + str(self.data_sats) + 'SATS'
        return stat.encode('utf-8')
        
    def fmt_datetimeOSDate(self, utc, timezone, fmt):
        '''returns input of float utc as string in formated time
           relys on OS for date which is important for daylight savings'''
        utc = str(utc)
        #SECONDS SINCE EPOCH
        hour = int(utc[0:2])
        min = int(utc[2:4])
        sec = int(utc[4:6])
        date = strftime('%d%m%Y', gmtime())
        day = int(date[0:2])
        month = int(date[2:4])
        year = int(date[4:8])
        epoch = timegm((year, month, day, hour, min, sec)) #convert time to seconds since epoch
        prdatetimeOSDate = self.fmt_datetime(epoch, timezone, fmt)
        prdatetimeOSDate.encode('utf-8')
       
    def fmt_datetime(self, timezone="Local - from OS", fmt="24H:M:S"):
        '''returns input of float utc as string in formated time
           relys on OS for date which is important for daylight savings
           example:  fmt_datetime(1287216960, '%I:%M:%S %p') produces 05:03:59 PM
           example:  fmt_datetime(1287216960, '%b. %d, %Y') produces Mar. 13, 2010'''
           
        '''%a     Locale's abbreviated weekday name.      
           %A     Locale's full weekday name.      
           %b     Locale's abbreviated month name.      
           %B     Locale's full month name.      
           %c     Locale's appropriate date and time representation.      
           %d     Day of the month as a decimal number [01,31].      
           %H     Hour (24-hour clock) as a decimal number [00,23].      
           %I     Hour (12-hour clock) as a decimal number [01,12].      
           %j     Day of the year as a decimal number [001,366].      
           %m     Month as a decimal number [01,12].      
           %M     Minute as a decimal number [00,59].      
           %p     Locale's equivalent of either AM or PM.     (1)
           %S     Second as a decimal number [00,61].     (2)
           %U     Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.     (3)
           %w     Weekday as a decimal number [0(Sunday),6].      
           %W     Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.     (3)
           %x     Locale's appropriate date representation.      
           %X     Locale's appropriate time representation.      
           %y     Year without century as a decimal number [00,99].      
           %Y     Year with century as a decimal number.      
           %Z     Time zone name (no characters if no time zone exists).      
           %%     A literal '%' character.
           Other ways to format:
                  DD-MM-YY
                  MM-DD-YY
                  Month, DD YYYY
                  Weekday, Month DD, YYYY
                  24H:M
                  24H:M:S
                  24H M S
                  12H:M AMPM
                  12H:M:S AMPM'''
        if self.data_epochUtc is None:
            return None
        else:
            epoch = self.data_epochUtc        
            if fmt == "DD-MM-YY":
                fmt = '%d-%m-%y'
            if fmt == "MM-DD-YY":
                fmt = '%m-%d-%y'
            if fmt == "Month, DD YYYY":
                fmt = '%b, %d %Y'
            if fmt == "Weekday, Month DD, YYYY":
                fmt = '%A, %b %d, %Y' 
            if fmt == "24H:M":
                fmt = '%H:%M'
            if fmt == "24H:M:S":
                fmt = '%H:%M:%S'
            if fmt == "24H M S":
                fmt = '%H %M %S'
            if fmt == "12H:M AMPM":
                fmt = '%I:%M %p'
            if fmt == "12H:M:S AMPM":
                fmt = '%I:%M:%S %p'
            if timezone == 'UTC' or timezone == 'GMT':
                stime = gmtime(epoch)
            if timezone == 'Local - from OS':
                stime = localtime(epoch)
            prdatetime = strftime(fmt, stime)
            return prdatetime.encode('utf-8')
    
    def fmt_lon(self, fmt='DMM'):
        '''returns string in fmt DDD or DMM or DMS rounded to less than 1 foot @ equator'''
        if self.data_long is None:
            return None
        else:
            lon = self.data_long
            if fmt == 'DDD': #.000001 is roughly .4 feet @ equator
                if lon > 0.0:
                    prlon = str(lon) + u'\u00B0E'
                if lon < 0.0:
                    prlon = str(-lon) + u'\u00B0W'
                if lon == 0.0:
                    prlon = str(lon) + u'\u00B0'
                return prlon.encode('utf-8')
            if fmt == 'DMM': #.0001 minute is roughly .6 feet @ equator
                deg = int(lon)
                min = lon - deg
                min = round((min * 60), 4) #this does not actually round up or down
                if deg < 0.0:
                    prlon = str(-(deg)) + u'\u00B0' + str(-(min)) + '\'W'
                if deg == 0.0:
                    prlon = str(deg) + u'\u00B0' + str(min) + '\''
                if deg > 0.0:
                    prlon = str(deg) + u'\u00B0' + str(min) + '\'E'
                return prlon.encode('utf-8')
            if fmt == 'DMS': #.001 second is roughly 1 foot @ equator
                deg = int(lon)
                mnn = (lon - deg) * 60
                min = int(mnn)
                sec = round(((mnn - min) * 60), 3)
                if deg < 0.0:
                    prlon = str(-(deg)) +  u'\u00B0' + str(-(min)) + '\'' + str(-(sec)) + '\"W'
                if deg == 0.0:
                    prlon = str(deg) +  u'\u00B0' + str(min) + '\'' + str(sec) + '\"'
                if deg > 0.0:
                    prlon = str(deg) +  u'\u00B0' + str(min) + '\'' + str(sec) + '\"E'
                return prlon.encode('utf-8')
    
    def fmt_lat(self, fmt='DMM'):
        '''returns string in fmt DDD or DMM or DMS rounded to less than 1 foot @ equator'''
        if self.data_lat is None:
            return None
        else:
            lat = self.data_lat
            if fmt == 'DDD': #.000001 is roughly .4 feet @ equator
                if lat > 0.0:
                    prlat = str(lat) + u'\u00B0N'
                if lat < 0.0:
                    prlat = str(-lat) + u'\u00B0S'
                if lat == 0.0:
                    prlat = str(lat) + u'\u00B0'
                return prlat.encode('utf-8')
            if fmt == 'DMM': #.0001 minute is roughly .6 feet @ equator
                deg = int(lat)
                min = lat - deg
                min = round((min * 60), 4) #this does not actually round up or down
                if deg < 0.0:
                    prlat = str(-(deg)) + u'\u00B0' + str(-(min)) + '\'S'
                if deg == 0.0:
                    prlat = str(deg) + u'\u00B0' + str(min) + '\''
                if deg > 0.0:
                    prlat = str(deg) + u'\u00B0' + str(min) + '\'N'
                return prlat.encode('utf-8')
            if fmt == 'DMS': #.001 second is roughly 1 foot @ equator
                deg = int(lat)
                mnn = (lat - deg) * 60
                min = int(mnn)
                sec = round(((mnn - min) * 60), 3)
                if deg < 0.0:
                    prlat = str(-(deg)) +  u'\u00B0' + str(-(min)) + '\'' + str(-(sec)) + '\"S'
                if deg == 0.0:
                    prlat = str(deg) +  u'\u00B0' + str(min) + '\'' + str(sec) + '\"'
                if deg > 0.0:
                    prlat = str(deg) +  u'\u00B0' + str(min) + '\'' + str(sec) + '\"N'
                return prlat.encode('utf-8')
    
    def fmt_sog(self, fmt='KTS'):
        '''returns string in fmt KTS or MPH or KPH rounded to the tenth'''
        if self.data_sog is None:
            return None
        else:
            sog = self.data_sog
            if fmt == 'KTS':
                sog = round(sog, 1)
                sog = str(sog) + ' KTS'
            if fmt == 'MPH':
                sog = round((sog * 1.15077945), 1)
                sog = str(sog) + ' MPH'
            if fmt == 'KPH':
                sog = round((sog * 1.852), 1)
                sog = str(sog) + ' KPH'
            return sog.encode('utf-8')          
        
    def fmt_cog(self):
        '''returns string for course over ground with NSEW directions'''
        if self.data_cog is None:
            return None
        else:
            cog = self.data_cog
            if cog > 348.75 or cog <= 11.25:
                dir = u'\u00B0 N'
            if cog > 11.25 and cog <= 33.75:
                dir = u'\u00B0 NNE'
            if cog > 33.75 and cog <= 56.25:
                dir = u'\u00B0 NE'
            if cog > 56.25 and cog <= 78.75:
                dir = u'\u00B0 ENE'
            if cog > 78.75 and cog <= 101.25:
                dir = u'\u00B0 E'
            if cog > 101.25 and cog <= 123.75:
                dir = u'\u00B0 ESE'
            if cog > 123.75 and cog <= 146.25:
                dir = u'\u00B0 SE'
            if cog > 146.25 and cog <= 168.75:
                dir = u'\u00B0 SSE'
            if cog > 168.75 and cog <= 191.25:
                dir = u'\u00B0 S'
            if cog > 191.25 and cog <= 213.75:
                dir = u'\u00B0 SSW'
            if cog > 213.75 and cog <= 236.25:
                dir = u'\u00B0 SW'
            if cog > 236.25 and cog <= 258.75:
                dir = u'\u00B0 WSW'
            if cog > 258.75 and cog <= 281.25:
                dir = u'\u00B0 W'
            if cog > 281.25 and cog <= 303.75:
                dir = u'\u00B0 WNW'
            if cog > 303.75 and cog <= 326.25:
                dir = u'\u00B0 NW'
            if cog > 326.25 and cog <= 348.75:
                dir = u'\u00B0 NNW'
            if cog == '999':
                dir = ''
            prcog = str(cog) + dir
            return prcog.encode('utf-8')
    
    def fmt_alt(self, fmt='METERS'):
        '''returns string in fmt FEET or METERS rounded to the hundredth'''
        if self.data_altM is None:
            return None
        else:
            if fmt == 'METERS':
                alt = str(self.data_altM) + ' METERS'
            if fmt == 'FEET':
                alt = round((self.data_altM * 3.2808399), 2)
                alt = str(alt) + ' FEET'
            return alt.encode('utf-8')
        
    def rmc(self, line): #data instance is in the MainWindow class
        '''self.data_utc - float
           self.data_status - string
           self.data_lat - float
           self.data_long - float
           self.data_sog - float
           self.data_cog - float
           self.data_date - string
           self.data_decl - float
           self.data_epochUtc - int
        '''
        line = line.split(',')
        try:
            #DATE
            date = line[9]
            if date != '':
                self.data_date = line[9]
            #UTC
            utc = line[1]
            if utc != '':
                self.data_utc = utc
            #SECONDS SINCE EPOCH
            if date != '' and utc != '':
                hour = int(utc[0:2])
                min = int(utc[2:4])
                sec = int(utc[4:6])
                day = int(date[0:2])
                month = int(date[2:4])
                year = date[4:6]
                year = int(strftime('%Y', strptime(year, '%y'))) #convert 2 digit year to 4
                self.data_epochUtc = timegm((year, month, day, hour, min, sec)) #convert time to seconds since epoch
            #STATUS
            i = line[2]
            if i == 'A':
                self.data_status = 'ACTIVE'
            if i == 'V':
                self.data_status = 'VOID'  
            #LATITUDE
            i = line[3]
            if i != '':
                lat = atof(i)
                if line[4] == 'S':
                    lat = -lat
                deg = int(lat/100)
                min = lat - deg*100
                lat = deg + (min/60)            
                lat = round(lat, 6)
                self.data_lat = lat
            #LONGITUDE
            i = line[5]
            if i != '':
                long = atof(i)
                if line[6] == 'W':
                    long = -long
                deg = int(long/100)
                min = long - deg*100
                long = deg + (min/60)
                long = round(long, 6)
                self.data_long = long
            #SPEED OVER GROUND
            i = line[7]
            if i != '':
                self.data_sog = atof(i)
            #COURSE OVER GROUND
            i = line[8]
            if i != '':
                self.data_cog = round(atof(i), 2)
            #MAGNETIC DECLINATION
            i = line[10]
            if i != '':
                decl = atof(i)
                if line[11] == 'W':
                    decl = atof(-decl)
                self.data_decl = decl
            self.rmcCount += 1
        except:
            print 'rmc - GPS sending malformed data:'
            print line
            
    def gga(self, line):#data instance is in the MainWindow class
        '''self.data_utc - float
           self.data_lat - float
           self.data_long - float
           self.data_sats - int
           self.data_hdop - float
           self.data_altM - float
        '''
        line = line.split(',')
        try:
            #UTC
            i = line[1]
            if i != '':
                utc = atof(i)
                self.data_utc = utc
            #LATITUDE
            i = line[2]
            if i != '':
                lat = atof(i)
                if line[3] == 'S':
                    lat = -lat
                deg = int(lat/100)
                min = lat - deg*100
                lat = deg + (min/60)            
                lat = round(lat, 6)
                self.data_lat = lat
            #LONGITUDE
            i = line[4]
            if i != '':
                long = atof(i)
                if line[5] == 'W':
                    long = -long
                deg = int(long/100)
                min = long - deg*100
                long = deg + (min/60)
                long = round(long, 6)
                self.data_long = long
            #SATELLITES IN VIEW
            i = line[7]
            if i !='':
                sats = int(line[7])
                self.data_sats = sats
            #HDOP
            i = line[8]
            if i != '':
                hdop = atof(line[8])
                self.data_hdop = hdop 
            #ALTITUDE (METERS)
            unit = line[10]
            alt = line[9]
            if unit == 'M' and alt != '':
                self.data_altM = atof(alt)
            self.ggaCount += 1
        except:
            print 'gga - GPS sending malformed data:'
            print line
            
    def vtg(self, line):
        '''self.data_sog - float
           self.data_cog - float
        '''
        line = line.split(',')
        try:
            #TRACK MADE GOOD/COURSE OVER GROUND (True)
            i = line[1]
            if line[2] == 'T' and i != '':
                self.data_cog = atof(i)
            #SPEED OVER GROUND (KNOTS) 
            i = line[5]   
            if line[6] == 'N' and i != '':
                self.data_sog = atof(i)
            self.vtgCount += 1
        except:
            print 'vtg - GPS sending malformed data:'
            print line
            
    def gsa(self, line):
        '''self.data_mode - string
           self.data_sats - int
           self.data_hdop - float
        '''
        line = line.split(',')
        try:
            #MODE
            #m0 = line[1] #auto or manual selectio of mode... we don't care about this
            i = line[2]
            if i != '':
                mode = int(line[2])
                if mode == 1:
                    self.data_mode = 'NO-FIX'
                if mode == 2:
                    self.data_mode = '2D-FIX'
                if mode == 3:
                    self.data_mode = '3D-FIX'
            #PRNS
            prns = line[3:15]
            #SATELLITES TRACKED
            sats = 0
            for each in prns:
                if each != '':
                    sats += 1
            self.data_sats = sats 
            #HDOP
            i = line[16]
            if i != '':
                self.data_hdop = atof(line[16])
            ''' we don't care about this yet
            #VDOP
            vdop = line[17]
            #PDOP
            pdop = line[18]
            e = pdop.find('*')
            pdop = pdop[0:e]
            '''
            self.gsaCount += 1
        except:
            print 'gsa - GPS sending malformed data:'
            print line

if __name__== "__main__":
    FILE = 'C:\\Documents and Settings\\User\\appdata\\local\\WinGippy\\recordings\\GPS_RECORDING_2.txt'
    COM = 'COM3'
    BAUD = 4800
    #GPS = gps(COM, BAUD, .5)
    GPS = gps(FILE, simloop=True)
    GPS.debug = True
    import os
    import threading
    threading.Timer(30, GPS.close).start() #schedule close in 30 seconds
      
    while GPS.alive.isSet():
        line =  GPS.rxline()
        #cmd = 'C:\\cygwin\\bin\\echo.exe \'%s\' > C:\\cygwin\\dev\\gpsfifo' %(line)
        #os.popen(cmd)
        print line
#        print GPS.data_raw
#        print GPS.fmt_lat(), GPS.fmt_lon()
#        print GPS.fmt_multistatus()
#        sleep(.5)
