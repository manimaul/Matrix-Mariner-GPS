import wx

class FancyFrame(wx.Frame):
    def __init__(self, bordercolor='#1BB2E0', fillcolor='#000000', rowht=60):
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, title='MMGPS', style = style)
        self.time = '00:00:00 AM'
        self.date = 'MON, JAN 00 0000'
        self.lat = '00'+u'\u00B0'+'00\'00.000"N'
        self.lon = '000'+u'\u00B0'+'00\'00.000"W'
        self.sog = '000.0 KTS'
        self.cog = '000.0'+u'\u00B0'+' NNN'
        self.alt = '00,000 FT'
        self.hdop = '0.0 HDOP'
#        self.labels = [('time',self.time),
#                       ('date',self.date),
#                       ('lat',self.lat),
#                       ('lon',self.lon),
#                       ('sog',self.sog),
#                       ('cog',self.cog),
#                       ('alt',self.alt),
#                       ('hdop',self.hdop)]
        self.labels = [('time',self.time),
                       ('sog',self.sog),
                       ('cog',self.cog)]
        
        self.fontface = 'Ubuntu'
        self.setextents(rowht)
        self.SetPosition((400,300))
        self.bordercolor = bordercolor
        self.fillcolor = fillcolor
                
        self.OptionsMenu = wx.Menu()
        self.settings = wx.MenuItem( self.OptionsMenu, wx.ID_ANY, u"Settings", wx.EmptyString, wx.ITEM_NORMAL )
        self.OptionsMenu.AppendItem( self.settings )
        
        self.colorMode = wx.MenuItem( self.OptionsMenu, wx.ID_ANY, u"Night Color Mode", wx.EmptyString, wx.ITEM_NORMAL )
        self.OptionsMenu.AppendItem( self.colorMode )
        
        self.kmlCtrl = wx.MenuItem( self.OptionsMenu, wx.ID_ANY, u"KML Control", wx.EmptyString, wx.ITEM_NORMAL )
        self.OptionsMenu.AppendItem( self.kmlCtrl )
        
        self.about = wx.MenuItem( self.OptionsMenu, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
        self.OptionsMenu.AppendItem( self.about )
        
        self.quit = wx.MenuItem( self.OptionsMenu, wx.ID_ANY, u"Quit", wx.EmptyString, wx.ITEM_NORMAL )
        self.OptionsMenu.AppendItem( self.quit )
        
        # Connect Events
        self.Bind( wx.EVT_MENU, self.showSettings, id = self.settings.GetId() )
        self.Bind( wx.EVT_MENU, self.switchColorMode, id = self.colorMode.GetId() )
        self.Bind( wx.EVT_MENU, self.showKMLCtrl, id = self.kmlCtrl.GetId() )
        self.Bind( wx.EVT_MENU, self.showAbout, id = self.about.GetId() )
        self.Bind( wx.EVT_MENU, self.killAll, id = self.quit.GetId() )
        self.Bind(wx.EVT_CONTEXT_MENU, self.MainWindowOnContextMenu)
        
        self.Bind(wx.EVT_MOTION, self.OnMouse)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()
            
    def setextents(self, rowht):
        self.radius = rowht/5
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)
        maxchar = 12
        maxstring = '0'*maxchar
        dc.SetFont(wx.FFontFromPixelSize((99, rowht), wx.SWISS, face=self.fontface))
        w,h = dc.GetTextExtent(maxstring)
        fh = rowht
        while h < rowht:
            fh += 1
            dc.SetFont(wx.FFontFromPixelSize((99, fh), wx.SWISS, face=self.fontface))
            w,h = dc.GetTextExtent(maxstring)
        self.fontsz = (99,fh)
        rows = self.labels.__len__()
        self.SetSize((w, rowht*rows))
        
    def showSettings(self, event):
        event.Skip()
    
    def switchColorMode(self, event):
        event.Skip()
    
    def showKMLCtrl(self, event):
        event.Skip()
    
    def showAbout(self, event):
        event.Skip()
    
    def killAll(self, event):
        event.Skip()
                
    def SetRoundShape(self, event=None):
        w, h = self.GetSizeTuple()
        self.SetShape(self.GetRoundShape(w,h,10))
        
    def GetRoundShape(self,w,h,r):
        return wx.RegionFromBitmap( self.GetRoundBitmap(w,h,r))
        
    def GetRoundBitmap(self,w,h,r):
        maskColor = wx.Color(0,0,0) #makes sharp corners transparent
        shownColor = wx.Color(5,5,5)
        b = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(b)
        dc.SetBrush(wx.Brush(maskColor))
        dc.DrawRectangle(0,0,w,h)
        dc.SetBrush(wx.Brush(shownColor))
        dc.SetPen(wx.Pen(shownColor))
        dc.DrawRoundedRectangle(0,0,w,h,r)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour(maskColor)
        return b
        
    def OnPaint(self, event):
        self.UpdateLabelList()
        #WINDOW
        #dc = wx.PaintDC(self)
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)
        
        w, h = self.GetSizeTuple()
        #pen = wx.Pen(self.bordercolor, width=1)
        #dc.SetPen(pen)
        dc.SetBrush(wx.Brush(self.fillcolor))
        dc.DrawRoundedRectangle(0, 0, w+1, h+1, self.radius)
        
        #INNER RECTANGLE
        xx,yy,ww,hh = self.InnerRectangle()
        #dc.SetPen(wx.RED_PEN)
        #dc.DrawRectangle(xx,yy,ww,hh)
        
        #CONTENT
        dc.SetTextForeground(self.bordercolor)
        
        pen = wx.Pen(self.bordercolor, width=1)
        dc.SetPen(pen)
        
        i=0
        rows = self.labels.__len__()
        for each in self.GetBoxes(ww,hh,rows,xx,yy):
            x,y,w,h,r=(each)
            #dc.DrawRoundedRectangle(x,y,w,h,r)
            if i != rows-1: #don't draw last line
                dc.DrawLine(x,y+h,x+w,y+h)
            
            #TEXT
            fw,fh = self.fontsz          
            label = self.labels[i]
            if label[0] == 'sog':
                dc.SetFont(wx.FFontFromPixelSize((fw/2, fh/2), wx.SWISS, face=self.fontface))
                dc.DrawLabel('SOG', (x,y,w,h), alignment=wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)
            if label[0] == 'cog':
                dc.SetFont(wx.FFontFromPixelSize((fw/2, fh/2), wx.SWISS, face=self.fontface))
                dc.DrawLabel('COG', (x,y,w,h), alignment=wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)
            if label[0] == 'alt':
                dc.SetFont(wx.FFontFromPixelSize((fw/2, fh/2), wx.SWISS, face=self.fontface))
                dc.DrawLabel('ALTITUDE', (x,y,w,h), alignment=wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)
            dc.SetFont(wx.FFontFromPixelSize(self.fontsz, wx.SWISS, face=self.fontface))
            dc.DrawLabel(label[1], (x,y,w,h), alignment=wx.ALIGN_LEFT)
            i+=1
    
    def UpdateLabelList(self):
#        self.labels = [('time',self.time),
#                       ('date',self.date),
#                       ('lat',self.lat),
#                       ('lon',self.lon),
#                       ('sog',self.sog),
#                       ('cog',self.cog),
#                       ('alt',self.alt),
#                       ('hdop',self.hdop)]
        
        self.labels = [('time',self.time),
                       ('sog',self.sog),
                       ('cog',self.cog)]
        
    def OnMouse(self, event):
        """implement dragging"""
        if not event.Dragging():
            self._dragPos = None
            return
        self.CaptureMouse()
        if not self._dragPos:
            self._dragPos = event.GetPosition()
        else:
            pos = event.GetPosition()
            displacement = self._dragPos - pos
            self.SetPosition( self.GetPosition() - displacement )
        self.ReleaseMouse()
    
    def InnerRectangle(self):
        w,h = self.GetSize()
        xx = int(round(.025*w, 0)) #5% of w
        yy = 1
        ww = int(round(.95*w, 0)) #95% of w
        hh = h-3
        return (xx,yy,ww,hh)
        
    def GetBoxes(self,width,height,boxes,xx,yy):
        '''return a list of box x,y and dimension tuples to fit into specified height
           **1/3 of a box height will be un-used**
        '''
        boxlist = []
        bxht = int(round(height/boxes, 0))
        remain = bxht*boxes-height
        for _ in range(boxes):
            if remain < 0:
                add = 1
            elif remain > 0:
                add = -1
            else:
                add = 0
            boxlist.append((xx,yy,width,bxht+add, self.radius))
            yy+=bxht+add
            remain += add
        return boxlist
    
    def MainWindowOnContextMenu(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.OptionsMenu, pos)
        
if __name__=='__main__':
    import threading
    print 'hello'
    def tock():
        import time
        while 1:
            frame.date = time.strftime('%a, %b %d %Y', time.localtime())
            frame.time = time.strftime('%I:%M:%S %p', time.localtime())
            time.sleep(1)
#            ht = frame.GetSize()[0]/9
#            frame.setextents(ht-1)
            frame.Refresh()
    app = wx.App()
    wx.SetDefaultPyEncoding('utf-8')
    frame = FancyFrame()
    tick = threading.Thread(target=tock).start()
    frame.Show()
    frame.SetTransparent(190)
    app.MainLoop()