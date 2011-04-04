#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx
import UserSettings

class KML_Ctrl(wx.MiniFrame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP
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
#        self.Bind(wx.EVT_BUTTON, self.go_hide, self.button_hide)
        self.Bind(wx.EVT_CLOSE, self.closed)

    def __set_properties(self):
        self.SetTitle("KML Control")
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
        self.button_zoomIn.SetToolTipString('Zoom In\rCurrent Range is: ' + UserSettings.kmlrange + ' Meters')
        self.button_zoomout.SetToolTipString('Zoom Out\rCurrent Range is: ' + UserSettings.kmlrange + ' Meters')
        self.button_dirNeg.SetToolTipString('Rotate View West\rCurrent View is: ' + UserSettings.kmlheading + '�')
        self.button_dirPos.SetToolTipString('Rotate View East\rCurrent View is: ' + UserSettings.kmlheading + '�')
        self.button_tiltUp.SetToolTipString('Tilt View Up\rCurrent View is: ' + UserSettings.kmltilt + '�')
        self.button_tiltDown.SetToolTipString('Tilt View Down\rCurrent View is: ' + UserSettings.kmltilt + '�')

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_tilt = wx.BoxSizer(wx.HORIZONTAL)
        sizer_dir = wx.BoxSizer(wx.HORIZONTAL)
        sizer_zoom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_zoom.Add(self.button_zoomIn, 0, wx.TOP|wx.BOTTOM, 1)
        sizer_zoom.Add(self.button_zoomout, 0, wx.TOP|wx.BOTTOM, 1)
        sizer_1.Add(sizer_zoom, 1, wx.EXPAND, 0)
        sizer_1.Add(self.button_course, 0, wx.TOP|wx.BOTTOM, 1)
        sizer_dir.Add(self.button_dirPos, 0, wx.TOP|wx.BOTTOM, 1)
        sizer_dir.Add(self.button_dirNeg, 0, wx.TOP|wx.BOTTOM, 1)
        sizer_1.Add(sizer_dir, 1, wx.EXPAND, 0)
        sizer_tilt.Add(self.button_tiltUp, 0, wx.TOP|wx.BOTTOM, 1)
        sizer_tilt.Add(self.button_tiltDown, 0, wx.TOP|wx.BOTTOM, 1)
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
        self.Hide()

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = KML_Ctrl(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
