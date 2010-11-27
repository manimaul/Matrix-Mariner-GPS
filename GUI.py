# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class MsgDialog
###########################################################################

class MsgDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.msg_txt = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.msg_txt.Wrap( -1 )
		self.bSizer10.Add( self.msg_txt, 0, wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.bSizer10.Add( self.m_button7, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.SetSizer( self.bSizer10 )
		self.Layout()
		self.bSizer10.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button7.Bind( wx.EVT_BUTTON, self.msgOK )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def msgOK( self, event ):
		event.Skip()
	

###########################################################################
## Class SettingsDialog
###########################################################################

class SettingsDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Settings", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.STAY_ON_TOP|wx.SYSTEM_MENU )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.gps_input_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.gps_input_panel = wx.Panel( self.gps_input_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.GPSInputChoice = wx.Choicebook( self.gps_input_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
		self.m_panel28 = wx.Panel( self.GPSInputChoice, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer3 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.gps_source_label = wx.StaticText( self.m_panel28, wx.ID_ANY, u"GPS Source", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.gps_source_label.Wrap( -1 )
		gSizer3.Add( self.gps_source_label, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		gps_source_comboChoices = []
		self.gps_source_combo = wx.ComboBox( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, gps_source_comboChoices, wx.CB_READONLY )
		gSizer3.Add( self.gps_source_combo, 0, wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.gps_baud_label = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Baud Rate", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.gps_baud_label.Wrap( -1 )
		gSizer3.Add( self.gps_baud_label, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		gps_baud_comboChoices = [ u"4800", u"9600", u"19200", u"38400", u"57600", u"115200" ]
		self.gps_baud_combo = wx.ComboBox( self.m_panel28, wx.ID_ANY, u"4800", wx.DefaultPosition, wx.DefaultSize, gps_baud_comboChoices, 0 )
		gSizer3.Add( self.gps_baud_combo, 0, wx.ALL, 5 )
		
		bSizer8.Add( gSizer3, 0, wx.EXPAND, 5 )
		
		self.m_panel28.SetSizer( bSizer8 )
		self.m_panel28.Layout()
		bSizer8.Fit( self.m_panel28 )
		self.GPSInputChoice.AddPage( self.m_panel28, u"Live GPS", True )
		self.m_panel29 = wx.Panel( self.GPSInputChoice, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )
		
		self.m_staticText26 = wx.StaticText( self.m_panel29, wx.ID_ANY, u"Select Recording:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		fgSizer1.Add( self.m_staticText26, 0, wx.ALL, 5 )
		
		replayListBoxChoices = []
		self.replayListBox = wx.ListBox( self.m_panel29, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, replayListBoxChoices, 0 )
		self.replayListBox.SetMinSize( wx.Size( 200,150 ) )
		
		fgSizer1.Add( self.replayListBox, 0, wx.ALL, 5 )
		
		self.m_staticText38 = wx.StaticText( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )
		fgSizer1.Add( self.m_staticText38, 0, wx.ALL, 5 )
		
		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_button8 = wx.Button( self.m_panel29, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		gbSizer2.Add( self.m_button8, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		fgSizer1.Add( gbSizer2, 1, wx.EXPAND, 5 )
		
		self.m_staticText361 = wx.StaticText( self.m_panel29, wx.ID_ANY, u"Loop Recording:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText361.Wrap( -1 )
		fgSizer1.Add( self.m_staticText361, 0, wx.ALL, 5 )
		
		self.replayLoop = wx.CheckBox( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.replayLoop.SetValue(True) 
		fgSizer1.Add( self.replayLoop, 0, wx.ALL, 5 )
		
		self.m_panel29.SetSizer( fgSizer1 )
		self.m_panel29.Layout()
		fgSizer1.Fit( self.m_panel29 )
		self.GPSInputChoice.AddPage( self.m_panel29, u"Recorded GPS", False )
		bSizer4.Add( self.GPSInputChoice, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.gps_input_apply = wx.Button( self.gps_input_panel, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.gps_input_apply, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.gps_input_panel.SetSizer( bSizer4 )
		self.gps_input_panel.Layout()
		bSizer4.Fit( self.gps_input_panel )
		self.gps_input_notebook.AddPage( self.gps_input_panel, u"GPS Input", False )
		self.output_panel = wx.Panel( self.gps_input_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_choicebook8 = wx.Choicebook( self.output_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
		self.kml_panel = wx.Panel( self.m_choicebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.kmlLabel = wx.StaticText( self.kml_panel, wx.ID_ANY, u"Google Earth (KML) Live GPS Tracking", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kmlLabel.Wrap( -1 )
		self.kmlLabel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer11.Add( self.kmlLabel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.kmlToggle = wx.ToggleButton( self.kml_panel, wx.ID_ANY, u"Start Tracking", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.kmlToggle, 0, wx.ALL, 5 )
		
		self.kmlLED = wx.StaticBitmap( self.kml_panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.kmlLED, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		bSizer11.Add( fgSizer4, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.kmlViewCheckbox = wx.CheckBox( self.kml_panel, wx.ID_ANY, u"KML View Control", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kmlViewCheckbox.Enable( False )
		
		bSizer11.Add( self.kmlViewCheckbox, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer51 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer51.SetFlexibleDirection( wx.BOTH )
		fgSizer51.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText29 = wx.StaticText( self.kml_panel, wx.ID_ANY, u"MMG.kml", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		self.m_staticText29.SetFont( wx.Font( 8, 74, 90, 92, False, "Tahoma" ) )
		
		fgSizer51.Add( self.m_staticText29, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText36 = wx.StaticText( self.kml_panel, wx.ID_ANY, u"will be placed on your Desktop.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText36.Wrap( -1 )
		fgSizer51.Add( self.m_staticText36, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )
		
		bSizer11.Add( fgSizer51, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer6 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText391 = wx.StaticText( self.kml_panel, wx.ID_ANY, u"Open with", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText391.Wrap( -1 )
		fgSizer6.Add( self.m_staticText391, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_hyperlink2 = wx.HyperlinkCtrl( self.kml_panel, wx.ID_ANY, u"Google Earth", u"http://earth.google.com", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		fgSizer6.Add( self.m_hyperlink2, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )
		
		bSizer11.Add( fgSizer6, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.kml_panel.SetSizer( bSizer11 )
		self.kml_panel.Layout()
		bSizer11.Fit( self.kml_panel )
		self.m_choicebook8.AddPage( self.kml_panel, u"Google Earth (KML)", True )
		self.gps_sharing_panel = wx.Panel( self.m_choicebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText30 = wx.StaticText( self.gps_sharing_panel, wx.ID_ANY, u"GPS virtual COM ports:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		self.m_staticText30.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer14.Add( self.m_staticText30, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		virtualListChoices = []
		self.virtualList = wx.ListBox( self.gps_sharing_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, virtualListChoices, 0 )
		self.virtualList.SetMinSize( wx.Size( 250,100 ) )
		
		bSizer14.Add( self.virtualList, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_button9 = wx.Button( self.gps_sharing_panel, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		fgSizer3.Add( self.m_button9, 0, wx.ALL, 5 )
		
		self.m_button10 = wx.Button( self.gps_sharing_panel, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		fgSizer3.Add( self.m_button10, 0, wx.ALL, 5 )
		
		bSizer14.Add( fgSizer3, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticline10 = wx.StaticLine( self.gps_sharing_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer14.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.tcpCheckbox = wx.CheckBox( self.gps_sharing_panel, wx.ID_ANY, u"GPS TCP Network Service", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tcpCheckbox.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer14.Add( self.tcpCheckbox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer7 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText40 = wx.StaticText( self.gps_sharing_panel, wx.ID_ANY, u"IP Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		fgSizer7.Add( self.m_staticText40, 0, wx.ALL, 5 )
		
		self.m_staticText392 = wx.StaticText( self.gps_sharing_panel, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText392.Wrap( -1 )
		fgSizer7.Add( self.m_staticText392, 0, wx.ALL, 5 )
		
		tcpAddrChoiceChoices = [ u"Any", u"127.0.0.1" ]
		self.tcpAddrChoice = wx.Choice( self.gps_sharing_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), tcpAddrChoiceChoices, 0 )
		self.tcpAddrChoice.SetSelection( 0 )
		fgSizer7.Add( self.tcpAddrChoice, 0, wx.ALL, 5 )
		
		self.tcpPortChoice = wx.TextCtrl( self.gps_sharing_panel, wx.ID_ANY, u"57757", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tcpPortChoice.SetMaxLength( 5 ) 
		self.tcpPortChoice.SetToolTipString( u"Valid port range: 49152 through 65535" )
		
		fgSizer7.Add( self.tcpPortChoice, 0, wx.ALL, 5 )
		
		bSizer14.Add( fgSizer7, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.gps_sharing_panel.SetSizer( bSizer14 )
		self.gps_sharing_panel.Layout()
		bSizer14.Fit( self.gps_sharing_panel )
		self.m_choicebook8.AddPage( self.gps_sharing_panel, u"GPS Sharing", False )
		self.gps_recording_panel = wx.Panel( self.m_choicebook8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText291 = wx.StaticText( self.gps_recording_panel, wx.ID_ANY, u"Record and save GPS input for later, simulated play back:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText291.Wrap( -1 )
		self.m_staticText291.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer17.Add( self.m_staticText291, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer5 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText32 = wx.StaticText( self.gps_recording_panel, wx.ID_ANY, u"Name GPS recording:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		fgSizer5.Add( self.m_staticText32, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.recName = wx.TextCtrl( self.gps_recording_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.recName.SetMinSize( wx.Size( 200,-1 ) )
		
		fgSizer5.Add( self.recName, 0, wx.ALL, 5 )
		
		self.m_staticText39 = wx.StaticText( self.gps_recording_panel, wx.ID_ANY, u"Recording status:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )
		fgSizer5.Add( self.m_staticText39, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.recStatus = wx.TextCtrl( self.gps_recording_panel, wx.ID_ANY, u"Recording off", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_READONLY )
		self.recStatus.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.recStatus.SetBackgroundColour( wx.Colour( 65, 65, 65 ) )
		self.recStatus.SetMinSize( wx.Size( 200,40 ) )
		
		fgSizer5.Add( self.recStatus, 0, wx.ALL, 5 )
		
		bSizer17.Add( fgSizer5, 0, 0, 5 )
		
		self.gbSizer1 = wx.GridBagSizer( 0, 0 )
		self.gbSizer1.SetFlexibleDirection( wx.BOTH )
		self.gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.recOutToggle = wx.ToggleButton( self.gps_recording_panel, wx.ID_ANY, u"Record", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.gbSizer1.Add( self.recOutToggle, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.recLED = wx.StaticBitmap( self.gps_recording_panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.gbSizer1.Add( self.recLED, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		bSizer17.Add( self.gbSizer1, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.gps_recording_panel.SetSizer( bSizer17 )
		self.gps_recording_panel.Layout()
		bSizer17.Fit( self.gps_recording_panel )
		self.m_choicebook8.AddPage( self.gps_recording_panel, u"GPS Recording Capture", False )
		bSizer10.Add( self.m_choicebook8, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.output_panel.SetSizer( bSizer10 )
		self.output_panel.Layout()
		bSizer10.Fit( self.output_panel )
		self.gps_input_notebook.AddPage( self.output_panel, u"Output", True )
		self.information_panel = wx.Panel( self.gps_input_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer2 = wx.GridSizer( 9, 2, 0, 0 )
		
		self.gpstimeCheckbox = wx.CheckBox( self.information_panel, wx.ID_ANY, u"GPS Time", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.gpstimeCheckbox.SetValue(True) 
		gSizer2.Add( self.gpstimeCheckbox, 0, wx.ALL, 5 )
		
		gpstimeChoiceChoices = [ u"24H:M", u"12H:M AMPM" ]
		self.gpstimeChoice = wx.Choice( self.information_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, gpstimeChoiceChoices, 0 )
		self.gpstimeChoice.SetSelection( 0 )
		gSizer2.Add( self.gpstimeChoice, 0, wx.ALL, 5 )
		
		self.timezone_label = wx.StaticText( self.information_panel, wx.ID_ANY, u"Time Zone", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.timezone_label.Wrap( -1 )
		gSizer2.Add( self.timezone_label, 0, wx.ALL, 5 )
		
		timezoneChoiceChoices = [ u"UTC", u"Local - from OS" ]
		self.timezoneChoice = wx.Choice( self.information_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, timezoneChoiceChoices, 0 )
		self.timezoneChoice.SetSelection( 1 )
		gSizer2.Add( self.timezoneChoice, 0, wx.ALL, 5 )
		
		self.dateCheckbox = wx.CheckBox( self.information_panel, wx.ID_ANY, u"Date", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.dateCheckbox.SetValue(True) 
		gSizer2.Add( self.dateCheckbox, 0, wx.ALL, 5 )
		
		dateChoiceChoices = [ u"Month, DD YYYY", u"Weekday, Month DD, YYYY", u"MM-DD-YY", u"DD-MM-YY" ]
		self.dateChoice = wx.Choice( self.information_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dateChoiceChoices, 0 )
		self.dateChoice.SetSelection( 0 )
		gSizer2.Add( self.dateChoice, 0, wx.ALL, 5 )
		
		self.latitudeCheckbox = wx.CheckBox( self.information_panel, wx.ID_ANY, u"Latitude", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.latitudeCheckbox.SetValue(True) 
		gSizer2.Add( self.latitudeCheckbox, 0, wx.ALL, 5 )
		
		lluChoiceChoices = [ u"DDD", u"DMM", u"DMS" ]
		self.lluChoice = wx.Choice( self.information_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lluChoiceChoices, 0 )
		self.lluChoice.SetSelection( 1 )
		gSizer2.Add( self.lluChoice, 0, wx.ALL, 5 )
		
		self.longitudeCheckbox = wx.CheckBox( self.information_panel, wx.ID_ANY, u"Longitude", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.longitudeCheckbox.SetValue(True) 
		gSizer2.Add( self.longitudeCheckbox, 0, wx.ALL, 5 )
		
		
		gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.sogCheckbox = wx.CheckBox( self.information_panel, wx.ID_ANY, u"Speed Over Ground", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sogCheckbox.SetValue(True) 
		gSizer2.Add( self.sogCheckbox, 0, wx.ALL, 5 )
		
		sogChoiceChoices = [ u"KTS", u"MPH", u"KPH" ]
		self.sogChoice = wx.Choice( self.information_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, sogChoiceChoices, 0 )
		self.sogChoice.SetSelection( 0 )
		gSizer2.Add( self.sogChoice, 0, wx.ALL, 5 )
		
		self.cogCheckbox = wx.CheckBox( self.information_panel, wx.ID_ANY, u"Course Over Ground", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cogCheckbox.SetValue(True) 
		gSizer2.Add( self.cogCheckbox, 0, wx.ALL, 5 )
		
		
		gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.altitudeCheckbox = wx.CheckBox( self.information_panel, wx.ID_ANY, u"Altitude", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.altitudeCheckbox.SetValue(True) 
		gSizer2.Add( self.altitudeCheckbox, 0, wx.ALL, 5 )
		
		altitudeChoiceChoices = [ u"METERS", u"FEET" ]
		self.altitudeChoice = wx.Choice( self.information_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, altitudeChoiceChoices, 0 )
		self.altitudeChoice.SetSelection( 0 )
		gSizer2.Add( self.altitudeChoice, 0, wx.ALL, 5 )
		
		self.hdopCheckbox = wx.CheckBox( self.information_panel, wx.ID_ANY, u"Horizontal Dilution of Position", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.hdopCheckbox.SetValue(True) 
		gSizer2.Add( self.hdopCheckbox, 0, wx.ALL, 5 )
		
		
		gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.information_panel.SetSizer( gSizer2 )
		self.information_panel.Layout()
		gSizer2.Fit( self.information_panel )
		self.gps_input_notebook.AddPage( self.information_panel, u"Information", False )
		self.appearance_panel = wx.Panel( self.gps_input_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 4, 2, 0, 0 )
		
		self.m_staticText18 = wx.StaticText( self.appearance_panel, wx.ID_ANY, u"Day Color", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		gSizer1.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		self.dayColorPicker = wx.ColourPickerCtrl( self.appearance_panel, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		gSizer1.Add( self.dayColorPicker, 0, wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self.appearance_panel, wx.ID_ANY, u"Night Color", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		gSizer1.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.nightColorPicker = wx.ColourPickerCtrl( self.appearance_panel, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		gSizer1.Add( self.nightColorPicker, 0, wx.ALL, 5 )
		
		self.m_staticText45 = wx.StaticText( self.appearance_panel, wx.ID_ANY, u"Font", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )
		gSizer1.Add( self.m_staticText45, 0, wx.ALL, 5 )
		
		fontComboChoices = [ u"Arial", u"Arial Black", u"Comic Sans MS", u"Courier New", u"Georgia", u"Impact", u"Lucida Console", u"Lucida Sans Unicode", u"Palatino Linotype", u"Tahoma", u"Times", u"Trebuchet MS", u"Verdana", u"Geneva", u"MS Serif", u"LCDDotMatrix5x8" ]
		self.fontCombo = wx.ComboBox( self.appearance_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, fontComboChoices, wx.CB_READONLY )
		gSizer1.Add( self.fontCombo, 0, wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self.appearance_panel, wx.ID_ANY, u"Size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		gSizer1.Add( self.m_staticText21, 0, wx.ALL, 5 )
		
		self.fontSizePicker = wx.SpinCtrl( self.appearance_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 8, 128, 23 )
		gSizer1.Add( self.fontSizePicker, 0, wx.ALL, 5 )
		
		bSizer3.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		self.appearance_reset = wx.Button( self.appearance_panel, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.appearance_reset, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.appearance_panel.SetSizer( bSizer3 )
		self.appearance_panel.Layout()
		bSizer3.Fit( self.appearance_panel )
		self.gps_input_notebook.AddPage( self.appearance_panel, u"Appearance", False )
		
		bSizer2.Add( self.gps_input_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline9 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.ok_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.SetSizer( bSizer2 )
		self.Layout()
		bSizer2.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.gps_source_combo.Bind( wx.EVT_ENTER_WINDOW, self.lookNewComs )
		self.m_button8.Bind( wx.EVT_BUTTON, self.recfDelete )
		self.replayLoop.Bind( wx.EVT_CHECKBOX, self.replayLoopPicked )
		self.gps_input_apply.Bind( wx.EVT_BUTTON, self.GPSInputApply )
		self.gps_input_apply.Bind( wx.EVT_LEFT_UP, self.applyGPSInput )
		self.kmlToggle.Bind( wx.EVT_TOGGLEBUTTON, self.kmlOut )
		self.kmlViewCheckbox.Bind( wx.EVT_CHECKBOX, self.showKMLCtrl_ )
		self.virtualList.Bind( wx.EVT_LISTBOX, self.setVirtualFocus )
		self.m_button9.Bind( wx.EVT_BUTTON, self.virtualAdd )
		self.m_button10.Bind( wx.EVT_BUTTON, self.virtualRemove )
		self.tcpCheckbox.Bind( wx.EVT_CHECKBOX, self.tcpCheck )
		self.tcpAddrChoice.Bind( wx.EVT_ENTER_WINDOW, self.tcpGetIP )
		self.tcpPortChoice.Bind( wx.EVT_TEXT, self.checkPortRegx )
		self.recName.Bind( wx.EVT_TEXT, self.recEnter )
		self.recOutToggle.Bind( wx.EVT_TOGGLEBUTTON, self.recOut )
		self.gpstimeCheckbox.Bind( wx.EVT_CHECKBOX, self.gpstimeAppear )
		self.gpstimeChoice.Bind( wx.EVT_CHOICE, self.gpstimePick )
		self.timezoneChoice.Bind( wx.EVT_CHOICE, self.timezonePick )
		self.dateCheckbox.Bind( wx.EVT_CHECKBOX, self.dateAppear )
		self.dateChoice.Bind( wx.EVT_CHOICE, self.datePick )
		self.latitudeCheckbox.Bind( wx.EVT_CHECKBOX, self.latitudeAppear )
		self.lluChoice.Bind( wx.EVT_CHOICE, self.lluPick )
		self.longitudeCheckbox.Bind( wx.EVT_CHECKBOX, self.longitudeAppear )
		self.sogCheckbox.Bind( wx.EVT_CHECKBOX, self.sogAppear )
		self.sogChoice.Bind( wx.EVT_CHOICE, self.sogPick )
		self.cogCheckbox.Bind( wx.EVT_CHECKBOX, self.cogAppear )
		self.altitudeCheckbox.Bind( wx.EVT_CHECKBOX, self.altitudeAppear )
		self.altitudeChoice.Bind( wx.EVT_CHOICE, self.altPick )
		self.hdopCheckbox.Bind( wx.EVT_CHECKBOX, self.hdopAppear )
		self.dayColorPicker.Bind( wx.EVT_COLOURPICKER_CHANGED, self.selectDayColor )
		self.nightColorPicker.Bind( wx.EVT_COLOURPICKER_CHANGED, self.selectNightColor )
		self.fontCombo.Bind( wx.EVT_COMBOBOX, self.chooseFont )
		self.fontSizePicker.Bind( wx.EVT_SPINCTRL, self.selectFontSize )
		self.fontSizePicker.Bind( wx.EVT_TEXT, self.selectFontSize )
		self.appearance_reset.Bind( wx.EVT_BUTTON, self.resetAppearance )
		self.ok_button.Bind( wx.EVT_BUTTON, self.settingsOK )
		self.ok_button.Bind( wx.EVT_LEFT_UP, self.hideSettingsDlg )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def lookNewComs( self, event ):
		event.Skip()
	
	def recfDelete( self, event ):
		event.Skip()
	
	def replayLoopPicked( self, event ):
		event.Skip()
	
	def GPSInputApply( self, event ):
		event.Skip()
	
	def applyGPSInput( self, event ):
		event.Skip()
	
	def kmlOut( self, event ):
		event.Skip()
	
	def showKMLCtrl_( self, event ):
		event.Skip()
	
	def setVirtualFocus( self, event ):
		event.Skip()
	
	def virtualAdd( self, event ):
		event.Skip()
	
	def virtualRemove( self, event ):
		event.Skip()
	
	def tcpCheck( self, event ):
		event.Skip()
	
	def tcpGetIP( self, event ):
		event.Skip()
	
	def checkPortRegx( self, event ):
		event.Skip()
	
	def recEnter( self, event ):
		event.Skip()
	
	def recOut( self, event ):
		event.Skip()
	
	def gpstimeAppear( self, event ):
		event.Skip()
	
	def gpstimePick( self, event ):
		event.Skip()
	
	def timezonePick( self, event ):
		event.Skip()
	
	def dateAppear( self, event ):
		event.Skip()
	
	def datePick( self, event ):
		event.Skip()
	
	def latitudeAppear( self, event ):
		event.Skip()
	
	def lluPick( self, event ):
		event.Skip()
	
	def longitudeAppear( self, event ):
		event.Skip()
	
	def sogAppear( self, event ):
		event.Skip()
	
	def sogPick( self, event ):
		event.Skip()
	
	def cogAppear( self, event ):
		event.Skip()
	
	def altitudeAppear( self, event ):
		event.Skip()
	
	def altPick( self, event ):
		event.Skip()
	
	def hdopAppear( self, event ):
		event.Skip()
	
	def selectDayColor( self, event ):
		event.Skip()
	
	def selectNightColor( self, event ):
		event.Skip()
	
	def chooseFont( self, event ):
		event.Skip()
	
	def selectFontSize( self, event ):
		event.Skip()
	
	
	def resetAppearance( self, event ):
		event.Skip()
	
	def settingsOK( self, event ):
		event.Skip()
	
	def hideSettingsDlg( self, event ):
		event.Skip()
	

###########################################################################
## Class SureDlg
###########################################################################

class SureDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.msgTxt = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.msgTxt.Wrap( -1 )
		self.bSizer12.Add( self.msgTxt, 0, wx.ALL, 5 )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.yes = wx.Button( self, wx.ID_ANY, u"Yes", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.yes, 0, wx.ALL, 5 )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.bSizer12.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		self.SetSizer( self.bSizer12 )
		self.Layout()
		self.bSizer12.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.exit )
		self.yes.Bind( wx.EVT_BUTTON, self.doYes )
		self.cancelButton.Bind( wx.EVT_BUTTON, self.doCcl )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def exit( self, event ):
		event.Skip()
	
	def doYes( self, event ):
		event.Skip()
	
	def doCcl( self, event ):
		event.Skip()
	

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"MMG", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.CLIP_CHILDREN )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		
		self.bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.gpstime = wx.StaticText( self, wx.ID_ANY, u"--:--", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.gpstime.Wrap( -1 )
		self.gpstime.SetFont( wx.Font( 14, 74, 90, 90, False, "Ubuntu" ) )
		self.gpstime.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.gpstime, 0, wx.LEFT|wx.TOP, 5 )
		
		self.gpstime_label = wx.StaticText( self, wx.ID_ANY, u"GPS TIME", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.gpstime_label.Wrap( -1 )
		self.gpstime_label.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.gpstime_label.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.gpstime_label, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		self.line1 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.bSizer1.Add( self.line1, 0, wx.ALL, 5 )
		
		self.gpsdate = wx.StaticText( self, wx.ID_ANY, u"---, -- ----", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.gpsdate.Wrap( -1 )
		self.gpsdate.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		self.gpsdate.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.gpsdate, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.gpsdate_label = wx.StaticText( self, wx.ID_ANY, u"DATE", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.gpsdate_label.Wrap( -1 )
		self.gpsdate_label.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.gpsdate_label.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.gpsdate_label, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		self.line2 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN )
		self.bSizer1.Add( self.line2, 0, wx.ALL, 5 )
		
		self.latitude = wx.StaticText( self, wx.ID_ANY, u"-- --.----' -", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.latitude.Wrap( -1 )
		self.latitude.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		self.latitude.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.latitude, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.latitude_label = wx.StaticText( self, wx.ID_ANY, u"LATITUDE", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.latitude_label.Wrap( -1 )
		self.latitude_label.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.latitude_label.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.latitude_label, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		self.line3 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN )
		self.bSizer1.Add( self.line3, 0, wx.ALL, 5 )
		
		self.longitude = wx.StaticText( self, wx.ID_ANY, u"-- --.----' -", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.longitude.Wrap( -1 )
		self.longitude.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		self.longitude.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.longitude, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.longitude_label = wx.StaticText( self, wx.ID_ANY, u"LONGITUDE", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.longitude_label.Wrap( -1 )
		self.longitude_label.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.longitude_label.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.longitude_label, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		self.line4 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.bSizer1.Add( self.line4, 0, wx.ALL, 5 )
		
		self.sog = wx.StaticText( self, wx.ID_ANY, u"-- ---", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.sog.Wrap( -1 )
		self.sog.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		self.sog.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.sog, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.sog_label = wx.StaticText( self, wx.ID_ANY, u"SOG", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.sog_label.Wrap( -1 )
		self.sog_label.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.sog_label.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.sog_label, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		self.line5 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN )
		self.bSizer1.Add( self.line5, 0, wx.ALL, 5 )
		
		self.cog = wx.StaticText( self, wx.ID_ANY, u"---.-- ---", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.cog.Wrap( -1 )
		self.cog.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		self.cog.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.cog, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.cog_label = wx.StaticText( self, wx.ID_ANY, u"COG", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.cog_label.Wrap( -1 )
		self.cog_label.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.cog_label.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.cog_label, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		self.line6 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN )
		self.bSizer1.Add( self.line6, 0, wx.ALL, 5 )
		
		self.altitude = wx.StaticText( self, wx.ID_ANY, u"- ------", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.altitude.Wrap( -1 )
		self.altitude.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		self.altitude.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.altitude, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.altitude_label = wx.StaticText( self, wx.ID_ANY, u"ALTITUDE", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.altitude_label.Wrap( -1 )
		self.altitude_label.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.altitude_label.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.altitude_label, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		self.line7 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN )
		self.bSizer1.Add( self.line7, 0, wx.ALL, 5 )
		
		self.hdop = wx.StaticText( self, wx.ID_ANY, u"----.--", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.hdop.Wrap( -1 )
		self.hdop.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		self.hdop.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.hdop, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.hdop_label = wx.StaticText( self, wx.ID_ANY, u"HDOP", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.hdop_label.Wrap( -1 )
		self.hdop_label.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.hdop_label.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.hdop_label, 0, wx.ALIGN_RIGHT|wx.RIGHT, 5 )
		
		self.line8 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN )
		self.bSizer1.Add( self.line8, 0, wx.ALL, 5 )
		
		self.status = wx.StaticText( self, wx.ID_ANY, u"GPS - NOT CONNECTED", wx.DefaultPosition, wx.DefaultSize, 0|wx.CLIP_CHILDREN )
		self.status.Wrap( -1 )
		self.status.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.status.SetForegroundColour( wx.Colour( 51, 153, 255 ) )
		
		self.bSizer1.Add( self.status, 0, wx.ALL, 5 )
		
		self.SetSizer( self.bSizer1 )
		self.Layout()
		self.bSizer1.Fit( self )
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
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.MainWindowOnContextMenu ) 
		
		
		# Connect Events
		self.Bind( wx.EVT_SIZE, self.onResize )
		self.Bind( wx.EVT_MENU, self.showSettings, id = self.settings.GetId() )
		self.Bind( wx.EVT_MENU, self.switchColorMode, id = self.colorMode.GetId() )
		self.Bind( wx.EVT_MENU, self.showKMLCtrl, id = self.kmlCtrl.GetId() )
		self.Bind( wx.EVT_MENU, self.showAbout, id = self.about.GetId() )
		self.Bind( wx.EVT_MENU, self.killAll, id = self.quit.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onResize( self, event ):
		event.Skip()
	
	def showSettings( self, event ):
		event.Skip()
	
	def switchColorMode( self, event ):
		event.Skip()
	
	def showKMLCtrl( self, event ):
		event.Skip()
	
	def showAbout( self, event ):
		event.Skip()
	
	def killAll( self, event ):
		event.Skip()
	
	def MainWindowOnContextMenu( self, event ):
		self.PopupMenu( self.OptionsMenu, event.GetPosition() )
		

###########################################################################
## Class AboutDlg
###########################################################################

class AboutDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer8 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.mmgLogo = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer8.Add( self.mmgLogo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.title = wx.StaticText( self, wx.ID_ANY, u"MatrixMariner GPS", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.title.Wrap( -1 )
		self.title.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer8.Add( self.title, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		self.bSizer13.Add( fgSizer8, 0, wx.ALIGN_CENTER_HORIZONTAL, 10 )
		
		self.m_staticText40 = wx.StaticText( self, wx.ID_ANY, u"(C) 2010 Will Kamp\nmanimaul@gmail.com", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		self.bSizer13.Add( self.m_staticText40, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_hyperlink2 = wx.HyperlinkCtrl( self, wx.ID_ANY, u"MatrixMariner.com", u"http://www.matrixmariner.com", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		self.bSizer13.Add( self.m_hyperlink2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, u"Features:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		self.m_staticText42.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		self.bSizer13.Add( self.m_staticText42, 0, wx.LEFT, 5 )
		
		self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"A simple, customizable and easy to read display\nof essential GPS data.\n\nShare your GPS over an unlimited number of virtual\nCOM ports or provide a TCP network service.\n\nCreate a KML network link to track GPS position\nlive using Google Earth. Control the zoom, tilt and\nview rotation.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		self.bSizer13.Add( self.m_staticText41, 0, wx.ALL, 5 )
		
		self.m_staticText43 = wx.StaticText( self, wx.ID_ANY, u"Requirements:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )
		self.m_staticText43.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		self.bSizer13.Add( self.m_staticText43, 0, wx.TOP|wx.LEFT, 5 )
		
		self.m_staticText44 = wx.StaticText( self, wx.ID_ANY, u"A standard NMEA0183 GPS.\n\nAt least RMC is recommended. GGA, VTG and GSA sentences also supported.\n\nRMC or (GGA, VTG) sentence required for fully functional KML output.\n\nAny and all serial data will be shared over virtual COM\nports and TCP service.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )
		self.bSizer13.Add( self.m_staticText44, 0, wx.ALL, 5 )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button11 = wx.Button( self, wx.ID_ANY, u"License", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer14.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button10 = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		self.bSizer13.Add( bSizer14, 1, wx.EXPAND, 5 )
		
		self.SetSizer( self.bSizer13 )
		self.Layout()
		self.bSizer13.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button11.Bind( wx.EVT_BUTTON, self.licPress )
		self.m_button10.Bind( wx.EVT_BUTTON, self.okPress )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def licPress( self, event ):
		event.Skip()
	
	def okPress( self, event ):
		event.Skip()
	

###########################################################################
## Class LicenseDlg
###########################################################################

class LicenseDlg ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel10 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.fgSizer8 = wx.FlexGridSizer( 2, 2, 0, 0 )
		self.fgSizer8.SetFlexibleDirection( wx.BOTH )
		self.fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.mmgLogo = wx.StaticBitmap( self.m_panel10, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fgSizer8.Add( self.mmgLogo, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.title = wx.StaticText( self.m_panel10, wx.ID_ANY, u"MatrixMariner GPS", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.title.Wrap( -1 )
		self.title.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		self.fgSizer8.Add( self.title, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.bSizer16.Add( self.fgSizer8, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText40 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"(C) 2010 Will Kamp\nmanimaul@gmail.com", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		self.bSizer16.Add( self.m_staticText40, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_hyperlink2 = wx.HyperlinkCtrl( self.m_panel10, wx.ID_ANY, u"MatrixMariner.com", u"http://www.matrixmariner.com", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		self.bSizer16.Add( self.m_hyperlink2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
		
		self.licText = wx.TextCtrl( self.m_panel10, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE|wx.TE_READONLY )
		self.licText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.licText.SetMinSize( wx.Size( 800,400 ) )
		
		self.bSizer16.Add( self.licText, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer81 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer81.SetFlexibleDirection( wx.BOTH )
		fgSizer81.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.agreeButton = wx.Button( self.m_panel10, wx.ID_ANY, u"I agree", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer81.Add( self.agreeButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.notagreeButton = wx.Button( self.m_panel10, wx.ID_ANY, u"I do not agree", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer81.Add( self.notagreeButton, 0, wx.ALL, 5 )
		
		self.bSizer16.Add( fgSizer81, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_panel10.SetSizer( self.bSizer16 )
		self.m_panel10.Layout()
		self.bSizer16.Fit( self.m_panel10 )
		bSizer15.Add( self.m_panel10, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer15 )
		self.Layout()
		bSizer15.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.agreeButton.Bind( wx.EVT_BUTTON, self.doOK )
		self.notagreeButton.Bind( wx.EVT_BUTTON, self.doQuit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def doOK( self, event ):
		event.Skip()
	
	def doQuit( self, event ):
		event.Skip()
	

