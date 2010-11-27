#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import wx
import GUI
import UserSettings
import threading
import Kml
import Tcp
import Gpscom
import RecordGps
from os import listdir, makedirs, remove, popen, write, path
from shutil import copy
from time import sleep
from sys import exit
from re import sub
from os.path import abspath
if UserSettings.opsys == 'Windows':
    from scanwin32 import basiccomlist
    from getIPwin import getIPAddressList

if UserSettings.opsys == 'Linux':
    from scanLin import basiccomlist
    from getIPlin import getIPAddressList

#----------------------------------------------------------------------
# Create an own event type, so that GUI updates can be delegated
# this is required as on some platforms only the main thread can
# access the GUI without crashing. wxMutexGuiEnter/wxMutexGuiLeave
# could be used too, but an event is more el
DATARX = wx.NewEventType()
# bind to serial data receive events
EVT_DATARX = wx.PyEventBinder(DATARX, 0)

class SerialRxEvent(wx.PyCommandEvent):
    eventType = DATARX
    def __init__(self, windowID, data, loc, action):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data
        self.loc = loc
        self.action = action
#----------------------------------------------------------------------

class Services:
    def __init__(self):
        self.myvs = False
        self.record = False
        self.recflag = False
        self.tcpdflag = False
        self.tcpd = False
        self.kmlflag = False
        self.gps = False

class KML_Ctrl(wx.MiniFrame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        wx.MiniFrame.__init__(self, *args, **kwds)
        self.button_zoomIn = wx.Button(self, -1, "In")
        self.button_zoomout = wx.Button(self, -1, "Out")
        self.button_course = wx.ToggleButton(self, -1, "Course")
        self.button_dirNeg = wx.Button(self, -1, ">")
        self.button_dirPos = wx.Button(self, -1, "<")
        self.button_tiltUp = wx.Button(self, -1, "Up")
        self.button_tiltDown = wx.Button(self, -1, "Dwn")
#        self.button_hide = wx.Button(self, -1, "Hide")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.go_zoomIn, self.button_zoomIn)
        self.Bind(wx.EVT_BUTTON, self.go_zoomOut, self.button_zoomout)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.go_course, self.button_course)
        self.Bind(wx.EVT_BUTTON, self.go_dirNeg, self.button_dirNeg)
        self.Bind(wx.EVT_BUTTON, self.go_dirPos, self.button_dirPos)
        self.Bind(wx.EVT_BUTTON, self.go_tiltUp, self.button_tiltUp)
        self.Bind(wx.EVT_BUTTON, self.go_tiltDown, self.button_tiltDown)
        self.Bind(wx.EVT_CLOSE, self.closed)

    def __set_properties(self):
        self.SetTitle("KML")
        self.button_zoomIn.SetMinSize((40, 27))
        self.button_zoomout.SetMinSize((40, 27))
        self.button_course.SetMinSize((80, -1))
        self.button_dirNeg.SetMinSize((40, 27))
        self.button_dirPos.SetMinSize((40, 27))
        self.button_tiltUp.SetMinSize((40, 27))
        self.button_tiltDown.SetMinSize((40, 27))
        self.set_tooltips()
        self.button_course.SetToolTipString('Course Mode\nLocks view rotation to course over ground')


    def set_tooltips(self):
        deg = u"\u00B0"
        self.button_zoomIn.SetToolTipString('Zoom In\rCurrent Range is: ' + UserSettings.kmlrange + ' Meters')
        self.button_zoomout.SetToolTipString('Zoom Out\rCurrent Range is: ' + UserSettings.kmlrange + ' Meters')
        self.button_dirNeg.SetToolTipString('Rotate View West\rCurrent View is: ' + UserSettings.kmlheading + deg)
        self.button_dirPos.SetToolTipString('Rotate View East\rCurrent View is: ' + UserSettings.kmlheading + deg)
        self.button_tiltUp.SetToolTipString('Tilt View Up\rCurrent View is: ' + UserSettings.kmltilt + deg)
        self.button_tiltDown.SetToolTipString('Tilt View Down\rCurrent View is: ' + UserSettings.kmltilt + deg)

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_tilt = wx.BoxSizer(wx.HORIZONTAL)
        sizer_dir = wx.BoxSizer(wx.HORIZONTAL)
        sizer_zoom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_zoom.Add(self.button_zoomIn, 0, wx.TOP | wx.BOTTOM, 1)
        sizer_zoom.Add(self.button_zoomout, 0, wx.TOP | wx.BOTTOM, 1)
        sizer_1.Add(sizer_zoom, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_course, 0, wx.TOP | wx.BOTTOM, 1)
        sizer_dir.Add(self.button_dirPos, 0, wx.TOP | wx.BOTTOM, 1)
        sizer_dir.Add(self.button_dirNeg, 0, wx.TOP | wx.BOTTOM, 1)
        sizer_1.Add(sizer_dir, 1, wx.EXPAND, 0)
        sizer_tilt.Add(self.button_tiltUp, 0, wx.TOP | wx.BOTTOM, 1)
        sizer_tilt.Add(self.button_tiltDown, 0, wx.TOP | wx.BOTTOM, 1)
        sizer_1.Add(sizer_tilt, 1, wx.EXPAND, 0)
#        sizer_1.Add(self.button_hide, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def go_zoomIn(self, event):
        val = int(UserSettings.kmlrange)
        if val > 10:
            val -= int(val * .25)
            UserSettings.kmlrange = str(val)
        self.set_tooltips()
        event.Skip()

    def go_zoomOut(self, event):
        val = int(UserSettings.kmlrange)
        if val < 10000000:
            val += int(val * .25)
            UserSettings.kmlrange = str(val)
        self.set_tooltips()
        event.Skip()

    def go_dirNeg(self, event):
        vals = UserSettings.kmlheading
        vali = int(vals)
        if vals[-1] != '0':
            vali = int(vals[0:-1] + '0')
        if vali > 0:
            vali -= 10
        else:
            vali = 350
        UserSettings.kmlheading = str(vali)
        self.set_tooltips()
        event.Skip()

    def go_dirPos(self, event): 
        vals = UserSettings.kmlheading
        vali = int(vals)
        if vals[-1] != '0':
            vali = int(vals[0:-1] + '0')
        if vali < 360:
            vali += 10
        else:
            vali = 10
#        self.text_ctrl_dir.SetValue(str(vali))
        UserSettings.kmlheading = str(vali)
        self.set_tooltips()
        event.Skip()

    def go_course(self, event):
        b = self.button_course
        s = b.GetValue()
        o = (self.button_dirNeg, self.button_dirPos)
        if s == True:
            UserSettings.kmlheading = '999'
            for each in o:
                each.SetToolTipString('View rotation is in Course Mode')
                each.Disable()
        else:
            UserSettings.kmlheading = '0'
            self.set_tooltips()
            for each in o:
                each.Enable()
        event.Skip()

    def go_tiltUp(self, event):
        vals = UserSettings.kmltilt
        val = int(vals)
        if vals[-1] != '5':
            val = int(round(val, -1))
        if val == 5:
            val = 0
        if val > 0:
            val -= 5
        UserSettings.kmltilt = str(val)
        self.set_tooltips()    

    def go_tiltDown(self, event):
        vals = UserSettings.kmltilt
        val = int(vals)
        if vals[-1] != '5':
            val = int(round(val, -1))
        if val == 85:
            val = 90
        if val < 90:
            val += 5
        UserSettings.kmltilt = str(val)
        self.set_tooltips()

    def go_hide(self, event): 
        self.Hide()
        event.Skip()
        
    def closed(self, event):
        SettingsDialog.kmlViewCheckbox.SetValue(0)
        self.Hide()
    
class SureDlg(GUI.SureDlg):
    def putMsg(self, title, s):
        self.s = s
        self.sel = SettingsDialog.replayListBox.GetString(s)
        self.selected = UserSettings.recrdir + self.sel + '.txt'
        msg = 'Are you certain you would like to remove ' + self.sel + ' ?\n' + \
              'This cannot be undone!'
        self.SetTitle(title)
        self.msgTxt.SetLabel(msg)
        self.bSizer12.Fit(self)
        self.ShowModal()
        app.SetTopWindow(self)
        self.SetFocus()
        self.file = file
        
    def doYes(self, event):
        print 'Deleting: ' + self.sel
        remove(self.selected)
        SettingsDialog.replayListBox.Delete(self.s)
        self.Destroy()

    def doCcl(self, event):
        self.Destroy()
        
    def exit(self, event):
        self.Destroy()
        
class MsgDialogSub(GUI.MsgDialog):
    '''Message Dialog - Event Overrides'''
    def msgOK(self, event):
        self.Hide()
        self.ok = True
        event.Skip()
    
    def postMsg(self, msg, title):
        self.SetTitle(title)
        self.msg_txt.SetLabel(msg)
        self.Layout()
        self.bSizer10.Fit(self)
        self.ShowModal()
        app.SetTopWindow(self)
        self.SetFocus()
    
    def bye(self, event):
        print 'bye'
        self.Destroy()
        event.Skip()
        
class LicenseDlgSub(GUI.LicenseDlg):
    def doOK(self, event):
        self.Hide()
        UserSettings.termsAgreed = True
        UserSettings.writecfg()
        MainWindow.Show()
        
    def doQuit(self, event):
        MainWindow.killAll(None)

class AboutDlgSub(GUI.AboutDlg):
    def okPress(self, event):
        self.Hide()
        
    def licPress(self, event):
        LicenseDlg.Show()
        SettingsDialog.Hide()
        MainWindow.Hide()
        self.Hide()
        pass

class SettingsDialogSub(GUI.SettingsDialog):
    '''Settings Dialog - Event Overrides'''
    def settingsOK(self, event):
        UserSettings.writecfg()
        self.Hide()
        event.Skip()
        
    def lookNewComs(self, event):
        lst = basiccomlist()
        selected = self.gps_source_combo.GetStringSelection() #get selection string
        SettingsDialog.gps_source_combo.SetItems(lst)
        i = SettingsDialog.gps_source_combo.FindString(selected)
        SettingsDialog.gps_source_combo.SetSelection(i)
        
    def closegps(self):
        if services.gps is not False:
            services.gps.close()
            print 'gps closed'
    
    def virtualAdd(self, event, comstr=''):
        if services.myvs is not False:
            name = services.myvs.createCOM(comstr)
            self.virtualList.Append(name)
            if comstr == '':
                UserSettings.vsps.append(name)
            print 'vsps', UserSettings.vsps
            services.vspeflag = True
        else:
            if UserSettings.opsys == 'Windows':
                msg = 'This feature is only available on 32bit versions of Windows.'
            if UserSettings.opsys == 'Linux':
                msg = 'An error occurred creating a virtual com port!'
            title = 'Sorry:'
            MsgDialog.postMsg(msg, title)
            
    def virtualRemove(self, event):        
            sel = self.virtualList.GetSelection()
            if sel > -1: #if one is actually selected
                for tpl in services.myvs.comlst: #tuple (vspe_int, COM#_string, serial_object)
                    if tpl[1] == self.virtualList.GetString(sel): #if COM#_string matches selection
                        #services.myvs.comlst.pop(self.myvs.comlst.index(tpl)) #remove tuple from list... this is done in removecom now
                        services.myvs.removeCOM(tpl) #close serial port and destroy
                        print 'removing' + tpl[1]
                        self.virtualList.Delete(sel) #remove from listbox
                        UserSettings.vsps.remove(tpl[1])
                        print 'vsps', UserSettings.vsps
                        if services.myvs.comlst.__len__() == 0:
                            services.vspeflag = False
        
    def GPSInputApply(self, event, auto=False):
        if auto:
            choice = 0
        else:
            choice = self.GPSInputChoice.GetSelection()
        self.closegps()
        if self.kmlToggle.GetValue():
            services.kmlflag = True
        else:
            services.kmlflag = False
        if choice == 0: #live GPS
            self.recOutToggle.Enable()
            if not self.recOutToggle: #if recording is off
                self.recStatus.SetValue('Recording off')
            elif self.recStatus.GetValue() == 'Recording disabled':
                self.recStatus.SetValue('Recording off')
            gpsCOM = self.gps_source_combo.GetValue() 
            gpsBaud = self.gps_baud_combo.GetValue()
            UserSettings.gpsCOM = gpsCOM
            UserSettings.gpsBaud = gpsBaud             
            print 'Connecting to: ' + gpsCOM
            if gpsCOM != '':
                self.gps_input_apply.Disable()
                services.gps = Gpscom.gps(gpsCOM, gpsBaud)
                threading.Timer(3, self.mutexReLayout).start()
                services.gps.setfreshtime(5) #set the data timeout
                self.datarxtxT = threading.Thread(target=self.datarxtx) #receives data to be transmitted as output
                self.datarxtxT.setName('datarxtx')
                self.datarxtxT.setDaemon(True) #python won't wait for it to terminate
                self.datarxT = threading.Thread(target=MainWindow.datarx)
                self.datarxT.setName('datarx')
                self.datarxT.setDaemon(True) #python won't wait for it to terminate
                self.datarxT.start()
                self.datarxtxT.start()
                self.gps_input_apply.Enable()
        if choice == 1: #recorded GPS
            self.recOutToggle.SetValue(False)
            self.stopRec()
            self.recStatus.SetValue('Recording disabled')
            self.recOutToggle.Disable()
            selected = self.replayListBox.GetSelection()
            if selected != -1:
                selected = self.replayListBox.GetString(selected)
                selected = UserSettings.recrdir + selected + '.txt'
                print 'Openning GPS replay file:'
                print selected
                services.gps = Gpscom.gps(selected, simloop=UserSettings.loopReplays)
                threading.Timer(3, self.mutexReLayout).start()
                services.gps.setfreshtime(15)#set the data timeout larger since stream is constant
                self.datarxtxT = threading.Thread(target=self.datarxtx) #receives data to be transmitted as output
                self.datarxtxT.setName('datarxtx')
                self.datarxT = threading.Thread(target=MainWindow.datarx)
                self.datarxT.setName('datarx')
                self.datarxT.start()
                self.datarxtxT.start()
                
    def datarxtx(self):
        while services.gps.alive.isSet():
            line = services.gps.rxline()
            #recording
            if services.recflag:
                services.record.rxline(line)
                str = services.record.getsize()
                wx.MutexGuiEnter()
                if services.recflag: #check again... needed for delay when switching to recording
                    self.recStatus.SetValue('Recording on\n' + str)
                wx.MutexGuiLeave()
            #vspe
            if services.vspeflag:
                services.myvs.write(line)
            #tcp
            if services.tcpdflag:
                services.tcpd.serveline(line)
            #kml
            if services.kmlflag:
                if UserSettings.kmlheading == '999' and services.gps.data_sog > 0.15:
                    cog = services.gps.data_cog
                else:
                    cog = UserSettings.kmlheading
                spd = services.gps.fmt_sog(UserSettings.sog_fmt)
                Kml.myserver.updateKML(services.gps.data_lat, services.gps.data_long, spd, cog, services.gps.data_altM, UserSettings.kmlrange, UserSettings.kmltilt)
        
    def gpstimePick(self, event):
        UserSettings.gpstime_fmt = self.gpstimeChoice.GetStringSelection()
        self.reLayout() #adjust window size for new data length
        
    def timezonePick(self, event):
        UserSettings.timezone = self.timezoneChoice.GetStringSelection()
        
    def datePick(self, event):
        UserSettings.gpsdate_fmt = self.dateChoice.GetStringSelection()
        self.reLayout() #adjust window size for new data length
        
    def lluPick(self, event):
        UserSettings.llu_fmt = self.lluChoice.GetStringSelection()
        self.reLayout() #adjust window size for new data length
        
    def sogPick(self, event):        
        UserSettings.sog_fmt = self.sogChoice.GetStringSelection()
        
    def altPick(self, event):
        UserSettings.alt_fmt = self.altitudeChoice.GetStringSelection()
        
    def gpstimeAppear(self, event):
        UserSettings.gpstime = self.gpstimeCheckbox.GetValue()
        self.allAppear()
    
    def dateAppear(self, event):         
        UserSettings.gpsdate = self.dateCheckbox.GetValue()
        self.allAppear()
        
    def latitudeAppear(self, event):         
        UserSettings.latitude = self.latitudeCheckbox.GetValue()
        self.allAppear()
        
    def longitudeAppear(self, event):         
        UserSettings.longitude = self.longitudeCheckbox.GetValue()
        self.allAppear()
        
    def sogAppear(self, event):         
        UserSettings.sog = self.sogCheckbox.GetValue()
        self.allAppear()
        
    def cogAppear(self, event):         
        UserSettings.cog = self.cogCheckbox.GetValue()
        self.allAppear()
    
    def altitudeAppear(self, event):         
        UserSettings.altitude = self.altitudeCheckbox.GetValue()
        self.allAppear()
        
    def hdopAppear(self, event):         
        UserSettings.hdop = self.hdopCheckbox.GetValue()
        self.allAppear()
    
    def allAppear(self):
        '''Show or Hide GPS information categories on MainWindow'''
        #show or hide gps time
        if UserSettings.gpstime == True:
            MainWindow.gpstime.Show()
            MainWindow.gpstime_label.Show()
            MainWindow.line1.Show()
        else:
            MainWindow.gpstime.Hide()
            MainWindow.gpstime_label.Hide()
            MainWindow.line1.Hide()
        #show or hide date
        if UserSettings.gpsdate == True:
            MainWindow.gpsdate.Show()
            MainWindow.gpsdate_label.Show()
            MainWindow.line2.Show()
        else:
            MainWindow.gpsdate.Hide()
            MainWindow.gpsdate_label.Hide()
            MainWindow.line2.Hide()
        #show or hide latitude
        if UserSettings.latitude == True:
            MainWindow.latitude.Show()
            MainWindow.latitude_label.Show()
            MainWindow.line3.Show()
        else:
            MainWindow.latitude.Hide()
            MainWindow.latitude_label.Hide()
            MainWindow.line3.Hide()
        #show or hide longitude
        if UserSettings.longitude == True:
            MainWindow.longitude.Show()
            MainWindow.longitude_label.Show()
            MainWindow.line4.Show()
        else:
            MainWindow.longitude.Hide()
            MainWindow.longitude_label.Hide()
            MainWindow.line4.Hide()
        #show or hide speed over ground
        if UserSettings.sog == True:
            MainWindow.sog.Show()
            MainWindow.sog_label.Show()
            MainWindow.line5.Show()
        else:
            MainWindow.sog.Hide()
            MainWindow.sog_label.Hide()
            MainWindow.line5.Hide()
        #show or hide couse over ground
        if UserSettings.cog == True:
            MainWindow.cog.Show()
            MainWindow.cog_label.Show()
            MainWindow.line6.Show()
        else:
            MainWindow.cog.Hide()
            MainWindow.cog_label.Hide()
            MainWindow.line6.Hide()
        #show or hide altitude
        if UserSettings.altitude == True:
            MainWindow.altitude.Show()
            MainWindow.altitude_label.Show()
            MainWindow.line7.Show()
        else:
            MainWindow.altitude.Hide()
            MainWindow.altitude_label.Hide()
            MainWindow.line7.Hide()
        #show or hide hdop
        if UserSettings.hdop == True:
            MainWindow.hdop.Show()
            MainWindow.hdop_label.Show()
            MainWindow.line8.Show()
        else:
            MainWindow.hdop.Hide()
            MainWindow.hdop_label.Hide()
            MainWindow.line8.Hide()
        #resize window
        self.reLayout()
        
    def mutexReLayout(self):
        wx.MutexGuiEnter()
        self.reLayout()
        wx.MutexGuiLeave()
        
    def reLayout(self):
        width, height = MainWindow.GetBestSizeTuple()
        size = (width + 75, height)
        MainWindow.SetSize(size)
        MainWindow.bSizer1.Fit(MainWindow)
        sleep(.1)
        MainWindow.onResize(None)
        
    def selectDayColor(self, event):
        UserSettings.daycolor = event.GetColour()
        if UserSettings.colormode == 'Day':
            self.setColors(UserSettings.daycolor)
        
    def selectNightColor(self, event):
        UserSettings.nightcolor = event.GetColour()
        if UserSettings.colormode == 'Night':
            self.setColors(UserSettings.nightcolor)
        
    def replaySetup(self):
        '''Fills recording listbox from recordings directory
           if directory is empty fill it with all files from \\rc\\recordings'''
        try:
            ls = listdir(UserSettings.recrdir) #~\\appdata\\local\\WinGippy\\recordings\\
        except OSError, WindowsError:
            makedirs(UserSettings.recrdir)
            ls = listdir(UserSettings.recrdir)
        if ls == []:
            print 'recordings director empty... filling'
            recdir = UserSettings.mrecdir
            for each in listdir(recdir):
                if each.endswith('.txt'):
                    copy(recdir + each, UserSettings.recrdir)
                    ls.append(each)
        for f in ls:
            print f
            self.replayListBox.Append(f[0:f.__len__() - 4])
        
    def recSetup(self):
        self.recName.SetValue(self.getNextRecFname())
        
    def getNextRecFname(self):
        '''Get the next recording file name'''
        list = listdir(UserSettings.recrdir) #~\\appdata\\local\\WinGippy\\recordings\\
        prefix = 'GPS_RECORDING_'
        fname = 'GPS_RECORDING_1'
        found = []
        dex = []
        for each in list:
            if each.find(prefix) != -1:
                found.append(each)    
        for each in found:
            each = each.lower()
            try:
                n = int(each[each.rfind('_') + 1:each.find('.txt')])
                dex.append(n)
            except ValueError:
                pass
        if dex != []:
            fname = prefix + str(max(dex) + 1)
        return fname
        
    def recfDelete(self, event):
        s = self.replayListBox.GetSelection()
        if s > -1:
            SureDlg(None).putMsg('Warning', s)
            
    def recEnter(self, event): #check for alphanumeric
        str = self.recName.GetValue()
        newstr = sub(r'\W+', '', str)
        if newstr != str:
            self.recName.SetValue(newstr)
            self.recName.SetInsertionPointEnd()
    
    def stopRec(self): #called from killall and inputapply when recording and when toggled off
        services.recflag = False
        if services.record != False: #if recording
            zero = services.record.bytes == 0 #bool, did the recording capture anything?             
            if not self.recfname in self.replayListBox.GetItems() and not zero: #dont append if overwriting existing
                self.replayListBox.Append(self.recfname)
            if not zero:
                self.recSetup() #get the next recording filename
            services.record.close()
            if zero:
                remove(UserSettings.recrdir + self.recfname + '.txt')
        services.record = False
        self.recOutToggle.SetValue(False) #unset toggle button   
        self.recLED.SetBitmap(self.greyLED)
        self.recStatus.SetValue('Recording off')
        self.recName.Enable()
        self.recOutToggle.SetLabel('Record')
    
    def recOut(self, event): #Record toggle button event
        if self.recName.GetValue() == '': #skip if filename field is empty
            self.recOutToggle.SetValue(False) #unset toggle button
        else:
            if self.recOutToggle.GetValue(): #start recording if Record button is set
                self.recLED.SetBitmap(self.redLED)
                self.recStatus.SetValue('Recording on')
                self.recOutToggle.SetLabel('Stop')
                self.recfname = self.recName.GetValue()
                recfname = self.recfname + '.txt'
                recfdir = UserSettings.recrdir
                services.record = RecordGps.record(recfdir, recfname)
                services.recflag = True
            else:
                self.stopRec()
                     
    def replayPickedSpeed(self, event):
        UserSettings.replaySpeed = self.replaySpeed.GetSelection() + 1
        
    def replayLoopPicked(self, event):  
        UserSettings.loopReplays = self.replayLoop.GetValue()
        
    def chooseFont(self, event):
        UserSettings.fontface = self.fontCombo.GetStringSelection()
        self.setFonts()
        
    def selectFont(self, event):
        mdsize = self.fontSizePicker.GetValue()
        UserSettings.mdfontsz = mdsize
        if mdsize >= 8 and mdsize < 10:
            UserSettings.smfontface = 'smallfonts'
            UserSettings.smfontsz = 4
        if mdsize >= 8 and mdsize < 14:
            UserSettings.smfontface = 'smallfonts'
            UserSettings.smfontsz = 6
        if mdsize >= 14 and mdsize < 35:
            UserSettings.smfontface = 'smallfonts'
            UserSettings.smfontsz = 8
        if mdsize >= 35:
            UserSettings.smfontface = 'smallfonts'
            UserSettings.smfontsz = 12
        self.setFonts()
        self.reLayout()
        
    def selectFontSize(self, event):
        self.selectFont(None)
            
    def setFonts(self):
        mdfont = wx.Font(UserSettings.mdfontsz, wx.SWISS, wx.NORMAL, wx.NORMAL, False, UserSettings.fontface)
        smfont = wx.Font(UserSettings.smfontsz, wx.SWISS, wx.NORMAL, wx.NORMAL, False, UserSettings.smfontface)
        
        MainWindow.gpstime.SetFont(mdfont)
        MainWindow.gpstime_label.SetFont(smfont)

        MainWindow.gpsdate.SetFont(mdfont)
        MainWindow.gpsdate_label.SetFont(smfont)
       
        MainWindow.latitude.SetFont(mdfont)
        MainWindow.latitude_label.SetFont(smfont)

        MainWindow.longitude.SetFont(mdfont)
        MainWindow.longitude_label.SetFont(smfont)
        
        MainWindow.sog.SetFont(mdfont)
        MainWindow.sog_label.SetFont(smfont)
        
        MainWindow.cog.SetFont(mdfont)
        MainWindow.cog_label.SetFont(smfont)
        
        MainWindow.altitude.SetFont(mdfont)
        MainWindow.altitude_label.SetFont(smfont)
        
        MainWindow.hdop.SetFont(mdfont)
        MainWindow.hdop_label.SetFont(smfont)
        
        MainWindow.status.SetFont(smfont)
        self.reLayout()
        
    def resetAppearance(self, event):        
        UserSettings.daycolor = (255, 159, 64)
        SettingsDialog.dayColorPicker.SetColour(UserSettings.daycolor)
        UserSettings.nightcolor = (155, 0, 0)
        SettingsDialog.nightColorPicker.SetColour(UserSettings.nightcolor)
        if UserSettings.colormode == 'Day':
            SettingsDialog.setColors(UserSettings.daycolor)
        else:
            SettingsDialog.setColors(UserSettings.nightcolor)
        UserSettings.mdfont = (UserSettings.mddefsz, UserSettings.fontface)
        UserSettings.smfont = (UserSettings.smdefsz, UserSettings.fontface)
        SettingsDialog.fontSizePicker.SetValue(UserSettings.mddefsz)
        SettingsDialog.setFonts()
            
    def setColors(self, color):
        MainWindow.gpstime.SetForegroundColour(color)
        MainWindow.gpstime_label.SetForegroundColour(color)

        MainWindow.gpsdate.SetForegroundColour(color)
        MainWindow.gpsdate_label.SetForegroundColour(color)
       
        MainWindow.latitude.SetForegroundColour(color)
        MainWindow.latitude_label.SetForegroundColour(color)

        MainWindow.longitude.SetForegroundColour(color)
        MainWindow.longitude_label.SetForegroundColour(color)
        
        MainWindow.sog.SetForegroundColour(color)
        MainWindow.sog_label.SetForegroundColour(color)
        
        MainWindow.cog.SetForegroundColour(color)
        MainWindow.cog_label.SetForegroundColour(color)
        
        MainWindow.altitude.SetForegroundColour(color)
        MainWindow.altitude_label.SetForegroundColour(color)
        
        MainWindow.hdop.SetForegroundColour(color)
        MainWindow.hdop_label.SetForegroundColour(color)
        
        MainWindow.status.SetForegroundColour(color)
        self.reLayout()
    
    def tcpGetIP(self, event):
        lst = getIPAddressList()
        lst.append('Any')
        selected = self.tcpAddrChoice.GetStringSelection() #get selection string
        self.tcpAddrChoice.SetItems(lst) #add list of any new machine ip addresses
        self.tcpAddrChoice.SetStringSelection(selected) #put selection back
        
    def checkPortRegx(self, event):
        port = str(self.tcpPortChoice.GetValue())
        newport = sub(r'\D+', '', port) #remove any non digits
        if newport != port:
            self.tcpPortChoice.SetValue(newport)
            self.tcpPortChoice.SetInsertionPointEnd()
                
    def checkPortVal(self):
        port = self.tcpPortChoice.GetValue()
        ok = True
        if port == '':
            self.tcpPortChoice.SetValue('57757')
            ok = False
        elif int(port) == 0:
            self.tcpPortChoice.SetValue('57757')
            ok = False
        else:
            self.tcpPortChoice.SetValue(str(int(port))) #removes leading zeros ... ex 000999
            n = int(port)
            if n > 65535:
                ok = False
                self.tcpPortChoice.SetValue('65535')
            if n < 49152:
                ok = False
                self.tcpPortChoice.SetValue('49152')
        if not ok:
            msg = 'Valid port range: 49152 through 65535'
            title = 'Attention:'
            MsgDialog.postMsg(msg, title)
            self.tcpPortChoice.SetFocus()
        return ok
        
    def tcpCheck(self, event):
        if self.tcpCheckbox.GetValue() and self.checkPortVal(): #is checked and valid port
            host = self.tcpAddrChoice.GetStringSelection()
            port = int(self.tcpPortChoice.GetValue())
            UserSettings.tcpip = host
            UserSettings.tcpport = port
            print 'starting tcp service on %s:%s' % (host, port)
            self.tcpd = Tcp.TCPd(host, port)
            self.tcpAddrChoice.Disable()
            self.tcpPortChoice.Disable()
            self.tcpdflag = True
        elif not self.tcpCheckbox.GetValue(): #unchecked
            print 'shutting down tcp service'
            self.tcpdflag = False
            self.tcpd.close()
            self.tcpAddrChoice.Enable()
            self.tcpPortChoice.Enable()
            UserSettings.tcpip = ''
            UserSettings.tcpport = 0
        else:
            self.tcpCheckbox.SetValue(False)
        
    def kmlOut(self, event):
        if self.kmlToggle.GetValue(): #kml is on
            services.kmlflag = True
            UserSettings.kml = True
            self.kmlLED.SetBitmap(self.redLED)
            self.kmlToggle.SetLabel('Stop Tracking')
            MainWindow.OptionsMenu.InsertItem(2, MainWindow.kmlCtrl)
            self.kmlViewCheckbox.Enable()
            Kml.myserver.createDesktopKML()
        else: #kml is off
            services.kmlflag = False
            UserSettings.kml = False
            self.kmlLED.SetBitmap(self.greyLED)
            self.kmlToggle.SetLabel('Start Tracking')
            MainWindow.OptionsMenu.RemoveItem(MainWindow.kmlCtrl)
            self.kmlViewCheckbox.Disable()
        
    def showKMLCtrl_(self, event):
        if self.kmlViewCheckbox.GetValue():
            KMLControl.Show()
        else:
            KMLControl.Hide()
               
class MainWindowSub(GUI.MainWindow):
    #----------------------------------------------------------------------
    # Functions to handle own event type
    # this is required as on some platforms only the main thread can
    # access the GUI without crashing. wxMutexGuiEnter/wxMutexGuiLeave
    # could be used too, but an event is more elegant.
    def OnEvent(self, event):
        text = event.data
        loc = event.loc
        action = event.action
        if action == 'label':
            oldtxt = loc.GetLabelText().encode('utf-8')
            if oldtxt != text: #reduces flickering on windows as text only updated if different
                loc.SetLabel(text)
        #if action == 'view':
        #    self.viewSettings()
            
    def bindEvents(self):
        self.Bind(EVT_DATARX, self.OnEvent)
       
    def LabelEvent(self, txt, loc):
        event = SerialRxEvent(self.GetId(), txt, loc, 'label')
        self.GetEventHandler().AddPendingEvent(event)
    #----------------------------------------------------------------------
        
    def blockSysColor(self, event):
        #block windows system color changes from 
        MainWindow.SetBackgroundColour(wx.Colour(0, 0, 0))
        print 'updating of the bg color from sys blocked'
        
    def datarx(self):
        if services.gps is not False:
            while services.gps.alive.isSet():
                time = services.gps.fmt_datetime(UserSettings.timezone, UserSettings.gpstime_fmt)
                self.LabelEvent(str(time), self.gpstime)
                
                date = services.gps.fmt_datetime(UserSettings.timezone, UserSettings.gpsdate_fmt)
                self.LabelEvent(str(date), self.gpsdate)
                
                lat = services.gps.fmt_lat(UserSettings.llu_fmt)
                self.LabelEvent(str(lat), self.latitude)
                
                long = services.gps.fmt_lon(UserSettings.llu_fmt)
                self.LabelEvent(str(long), self.longitude)
                
                sog = services.gps.fmt_sog(UserSettings.sog_fmt)
                self.LabelEvent(str(sog), self.sog)
                
                cog = services.gps.fmt_cog()
                self.LabelEvent(str(cog), self.cog)
                
                alt = services.gps.fmt_alt(UserSettings.alt_fmt)
                self.LabelEvent(str(alt), self.altitude)
                
                hdop = services.gps.data_hdop
                self.LabelEvent(str(hdop), self.hdop)
                
                stat = services.gps.fmt_multistatus()
                self.LabelEvent(str(stat), self.status)
                sleep(.3)
            #reset data when fished
            time = '--:--:--'
            self.LabelEvent(str(time), self.gpstime)
            
            date = '---, -- ----'
            self.LabelEvent(str(date), self.gpsdate)
            
            lat = '-- --.----\' -'
            self.LabelEvent(str(lat), self.latitude)
            
            long = '-- --.----\' -'
            self.LabelEvent(str(long), self.longitude)
            
            sog = '-- ---'
            self.LabelEvent(str(sog), self.sog)
            
            cog = '---.-- ---'
            self.LabelEvent(str(cog), self.cog)
            
            alt = '- ------'
            self.LabelEvent(str(alt), self.altitude)
            
            hdop = '----.--'
            self.LabelEvent(str(hdop), self.hdop)
            stat = 'NO DATA'
            self.LabelEvent(str(stat), self.status)
        
    def showSettings(self, event):
        SettingsDialog.Show()
        app.SetTopWindow(SettingsDialog)
        
    def showAbout(self, event):
        AboutDlg.Show()
        app.SetTopWindow(AboutDlg)
    
    def switchColorMode(self, event):
        if UserSettings.colormode == 'Day':
            print 'switching to night mode'
            UserSettings.colormode = 'Night'
            self.colorMode.SetItemLabel('Day Color Mode')
            SettingsDialog.setColors(UserSettings.nightcolor)
        else:
            print 'switching to day mode'
            UserSettings.colormode = 'Day'  
            self.colorMode.SetItemLabel('Night Color Mode') 
            SettingsDialog.setColors(UserSettings.daycolor)
            
    def killAll(self, event):
        print 'shutting down...'
        UserSettings.screenposition = self.GetScreenPosition()
        UserSettings.writecfg()
        
        if UserSettings.opsys == 'Windows': #this doesn't work in Linux... speeds up appearance of shutdown
            LicenseDlg.Hide()
            KMLControl.Hide()
            AboutDlg.Hide()
            MsgDialog.Hide()
            SettingsDialog.Hide()
            self.Hide()

        if services.gps is not False:
            print 'closing serial port'
            services.gps.close()
            print 'gps closed'
        
        print 'closing httpd'
        Kml.myserver.close()
        
        print 'stopping recording if it\'s active'
        SettingsDialog.stopRec()
        
        if services.myvs is not False:
            print 'closing VSPE-L'
            try:
                services.myvs.close() #try because this will not be included in 64bit
            except NameError:
                pass
        
        print 'number of running threads'
        print threading.activeCount()
                
        print 'destroying objects'
        try:
            LicenseDlg.Destroy()
            KMLControl.Destroy()
            AboutDlg.Destroy()
            MsgDialog.Destroy()
            SettingsDialog.Destroy()
            self.Destroy()
        except:
            print 'error... exiting'
            exit()
            
    def MainWindowOnContextMenu(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.OptionsMenu, pos)
        
    def showKMLCtrl(self, event):
        KMLControl.Show()
        SettingsDialog.kmlViewCheckbox.SetValue(True)
        
    def onResize(self, event):
        self.SetLines()
        self.Layout()
        
    def SetLines(self):
        lines = (self.line1, self.line2, self.line3, self.line4, self.line5, self.line6, self.line7, self.line8)
        w = MainWindow.bSizer1.GetSize()[0] - 10
        if UserSettings.colormode == 'Day':
            r,g,b=(100,100,100)
        else:
            r,g,b=(70,70,70)
        sepline = MainWindow.hline(r,g,b,w)
        for line in lines:
            line.SetBitmap(sepline)
    
    def hline(self, red=255, green=255, blue=255, width=100):
        color = wx.Colour(red, green, blue)
        mypen = wx.Pen(color)
        bmp  = wx.EmptyBitmap(width, 2)
        mem = wx.MemoryDC()
        mem.SelectObject(bmp)
        mem.SetBackground(wx.BLACK_BRUSH)  # allocates the space
        mem.Clear()
        mem.SetPen(mypen)
        mem.DrawLine(0,0,width,0)
        return bmp

def mmgRun():
    global app
    app = wx.App(False)
    wx.SetDefaultPyEncoding('utf-8')
    wx.InitAllImageHandlers()
    global services
    services = Services()  #Object to hold data services
    global KMLControl
    KMLControl = KML_Ctrl(None) #Object for KML Control dialog
    global MsgDialog
    MsgDialog = MsgDialogSub(None) #Object for message dialog
    MsgDialog.ok = False
    global AboutDlg
    AboutDlg = AboutDlgSub(None)
    global SettingsDialog
    SettingsDialog = SettingsDialogSub(None) #Object for settings dialog window
    global LicenseDlg
    LicenseDlg = LicenseDlgSub(None) #Object for license dialog 
    global MainWindow 
    MainWindow = MainWindowSub(None) #Object for main window
    MainWindow.SetDoubleBuffered(True) #Reduces flickering
    
    '''set the icons'''
    d = abspath(UserSettings.workdir + '/rc/mmg.ico')
    icon = wx.Icon(d, wx.BITMAP_TYPE_ICO)
    MainWindow.SetIcon(icon)
    MsgDialog.SetIcon(icon)
    AboutDlg.SetIcon(icon)
    SettingsDialog.SetIcon(icon)
    LicenseDlg.SetIcon(icon)
    
    '''about and license'''
    d = abspath(UserSettings.workdir + '/rc/mmg.png')
    AboutDlg.mmgpng = wx.Bitmap(d, wx.BITMAP_TYPE_ANY)
    AboutDlg.mmgLogo.SetBitmap(AboutDlg.mmgpng)
    AboutDlg.bSizer13.Fit(AboutDlg)
    AboutDlg.title.SetLabel('MatrixMariner GPS %s' %(UserSettings.version))
    AboutDlg.Layout()
    if UserSettings.opsys == 'Windows':
        d = abspath(UserSettings.workdir + '/rc/windowslicense.txt')
    if UserSettings.opsys == 'Linux':
        d = abspath(UserSettings.workdir + '/rc/linuxlicense.txt')
    f = open(d, 'r')
    lic = f.read()
    LicenseDlg.licText.SetValue(lic)
    f.close()
    LicenseDlg.title.SetLabel('MatrixMariner GPS %s' %(UserSettings.version))
    LicenseDlg.mmgLogo.SetBitmap(AboutDlg.mmgpng)
    LicenseDlg.bSizer16.Fit(LicenseDlg)
    LicenseDlg.Layout()
    
    '''virtual serial port emulation'''
    if UserSettings.opsys == 'Windows' and UserSettings.arch == 'x86':
        try:
            import VSPE
            services.myvs = VSPE.vspe()
            services.myvs.initialize()
        except:
            print 'VSPI driver not installed, installing...'
            msg = 'MMG needs to install a Virtual Serial Port Emulator Driver\r' + \
                  'This will only install once.'
            title = 'Attention'
            MsgDialog.postMsg(msg, title)
            while MsgDialog.IsShown():
                sleep(.1)
            if MsgDialog.ok:
                from subprocess import Popen, PIPE
                from os import chdir, getcwd
                chdir(getcwd()+'\\rc\\SetupVSPE\\')
                print getcwd()
                cmd = 'SetupVSPE.msi /qb'
                print cmd
                p = Popen(cmd, shell=True, stdout=PIPE)
                p.wait()
                lnk = UserSettings.homedir+'\\Desktop\\VSPE.lnk'
                while not path.isfile(lnk):
                    print 'waiting to delete:', lnk
                    sleep(1)
                remove(lnk)
                try:
                    import VSPE
                    services.myvs = VSPE.vspe()
                    services.myvs.initialize()
                except:
                    pass
    services.vspeflag = False
    if UserSettings.opsys == 'Linux':
        import VSPLin
        services.myvs = VSPLin.vsp(dir='/tmp/dev', pname='vgps')
    
    ''''fix some events '''
    MainWindow.Bind(wx.EVT_SYS_COLOUR_CHANGED, MainWindow.blockSysColor) #bind system color change event to Block other apps from changing color
    MainWindow.Bind(wx.EVT_CLOSE, MainWindow.killAll)
    MainWindow.Unbind(wx.EVT_RIGHT_DOWN) #override wx.EVT_RIGHT_DOWN in GUI automatically created by wxFB
    MainWindow.Bind(wx.EVT_CONTEXT_MENU, MainWindow.MainWindowOnContextMenu) #replace EVT_RIGHT_DOWN with this... works better
    #MainWindow.Bind(wx.EVT_SIZING, MainWindow.onResize)
    MainWindow.bindEvents() #bind events to custom event handler
    LicenseDlg.Bind(wx.EVT_CLOSE, MainWindow.killAll)
    
    '''read config file and layout main window and settings dialog'''
    UserSettings.readcfg()
    MainWindow.SetPosition(UserSettings.screenposition) 
    SettingsDialog.allAppear() #show hide gps information base on user settings (layout gets reset)
    SettingsDialog.setColors(UserSettings.daycolor)    
    MainWindow.OptionsMenu.RemoveItem(MainWindow.kmlCtrl) #don't show this menu item yet
    
    '''change settings dialog to reflect user config'''
    ###gps input tab###
    SettingsDialog.replaySetup() #Fills recording listbox from recordings directory if directory is empty fill it with all files from \\rc\\recordings
    SettingsDialog.recSetup() #Fills the recording filename field
    #SettingsDialog.replaySpeed.SetSelection(UserSettings.replaySpeed - 1)
    SettingsDialog.replayLoop.SetValue(UserSettings.loopReplays)
    
    ###gps output tab###
    d = abspath(UserSettings.workdir + '/rc/greyLED.png')
    SettingsDialog.greyLED = wx.Bitmap(d, wx.BITMAP_TYPE_ANY)
    d = abspath(UserSettings.workdir + '/rc/redLED.png')
    SettingsDialog.redLED = wx.Bitmap(d, wx.BITMAP_TYPE_ANY)
    SettingsDialog.recLED.SetBitmap(SettingsDialog.greyLED)
    SettingsDialog.kmlLED.SetBitmap(SettingsDialog.greyLED)
    
    ###information tab###
    SettingsDialog.gpstimeCheckbox.SetValue(UserSettings.gpstime) #check/uncheck gps time checkbox from user settings
    
    i = SettingsDialog.gpstimeChoice.FindString(UserSettings.gpstime_fmt)
    SettingsDialog.gpstimeChoice.SetSelection(i) #select gps time format from user settings
    
    i = SettingsDialog.timezoneChoice.FindString(UserSettings.timezone)
    SettingsDialog.timezoneChoice.SetSelection(i) #select timezone format from user settings
    
    SettingsDialog.dateCheckbox.SetValue(UserSettings.gpsdate) #check/uncheck date checkbox from user settings
    i = SettingsDialog.dateChoice.FindString(str(UserSettings.gpsdate_fmt))
    SettingsDialog.dateChoice.SetSelection(i) #select date format from user settings
    
    SettingsDialog.latitudeCheckbox.SetValue(UserSettings.latitude) #check/uncheck latitude checkbox from user settings
    i = SettingsDialog.lluChoice.FindString(UserSettings.llu_fmt)
    SettingsDialog.lluChoice.SetSelection(i) #select lat/long format from user settings
    SettingsDialog.longitudeCheckbox.SetValue(UserSettings.longitude) #check/uncheck longitude checkbox from user settings
    
    SettingsDialog.sogCheckbox.SetValue(UserSettings.sog) #check/uncheck speed over ground checkbox from user settings
    i = SettingsDialog.sogChoice.FindString(UserSettings.sog_fmt)
    SettingsDialog.sogChoice.SetSelection(i) #select sog format from user settings
    
    SettingsDialog.cogCheckbox.SetValue(UserSettings.cog) #check/uncheck course over ground checkbox from user settings
    
    SettingsDialog.altitudeCheckbox.SetValue(UserSettings.altitude) #check/uncheck altitude checkbox from user settings
    i = SettingsDialog.altitudeChoice.FindString(UserSettings.alt_fmt)
    SettingsDialog.altitudeChoice.SetSelection(i) #select altitide format from user settings
    
    SettingsDialog.hdopCheckbox.SetValue(UserSettings.hdop) #check/uncheck hdop checkbox from user settings
    
    ###appearance tab### 
    SettingsDialog.dayColorPicker.SetColour(UserSettings.daycolor)
    SettingsDialog.nightColorPicker.SetColour(UserSettings.nightcolor)
    if UserSettings.opsys == 'Linux':
        efonts = wx.FontEnumerator()
        efonts.EnumerateFacenames()
        listfonts = efonts.GetFacenames()
        listfonts.sort()
        SettingsDialog.fontCombo.SetItems(listfonts)
    SettingsDialog.fontCombo.SetStringSelection(UserSettings.fontface)
    SettingsDialog.fontSizePicker.SetValue(UserSettings.mdfontsz)
    SettingsDialog.chooseFont(None)
    
    ###kick it off###
    Kml.myserver = Kml.KMLServer()
    if UserSettings.termsAgreed:
        MainWindow.Show()
    else:
        LicenseDlg.Show()
    
    '''populate available input ports and autoconnect to last'''
    comlst = basiccomlist()
    SettingsDialog.gps_source_combo.SetItems(comlst)
    if comlst.__len__() > 0 and UserSettings.gpsCOM == '':
        i = SettingsDialog.gps_source_combo.FindString(comlst[-1])
        SettingsDialog.gps_source_combo.SetSelection(i)
    else:
        i = SettingsDialog.gps_source_combo.FindString(UserSettings.gpsCOM)
        SettingsDialog.gps_source_combo.SetSelection(i)
        SettingsDialog.autoconnect = wx.Timer(SettingsDialog)
        SettingsDialog.Bind(wx.EVT_TIMER, SettingsDialog.GPSInputApply(None, True), SettingsDialog.autoconnect)
        SettingsDialog.autoconnect.Start(milliseconds=2000, oneShot=True)
    
    '''auto-start tcpd, vspe, and/or kml if on last time'''
    if services.myvs != False:
        for vsp in UserSettings.vsps:
            if not comlst.__contains__(vsp): #don't create a virtual com that exists as a real one
                SettingsDialog.virtualAdd(None, vsp)
            else:
                UserSettings.vsps.remove(vsp)
            
    if UserSettings.tcpip != '' and UserSettings.tcpport > 0:
        SettingsDialog.tcpCheckbox.SetValue(True)
        SettingsDialog.tcpGetIP(None) #populate ips in tcpAddrChoice
        i = SettingsDialog.tcpAddrChoice.FindString(UserSettings.tcpip)
        SettingsDialog.tcpAddrChoice.SetSelection(i)
        SettingsDialog.tcpPortChoice.SetValue(str(UserSettings.tcpport))
        SettingsDialog.tcpCheck(None)
        
    if UserSettings.kml:
        SettingsDialog.kmlToggle.SetValue(True)
        SettingsDialog.kmlOut(None)
        
    app.MainLoop()
    
if __name__ == "__main__":
    import instance
    lock = instance.singleInst()
    if lock.single:
        mmgRun()
    else:
        app = wx.App(False)
        wx.SetDefaultPyEncoding('utf-8')
        wx.InitAllImageHandlers()
        msgdlg = MsgDialogSub(None)
        msgdlg.m_button7.Bind(wx.EVT_BUTTON, msgdlg.bye)
        msgdlg.Bind(wx.EVT_CLOSE, msgdlg.bye) 
        title = 'MMG'
        msg = 'Matrix Mariner GPS is already running!'
        msgdlg.postMsg(msg, title)
        app.MainLoop()
        
    

