#!/usr/bin/env python
#-*- coding:utf-8 -*-

import wx

# globals (these will be placed in a config file)
programName = 'Journey Volunteer Check-in'
programVersion = '0.0.1b'
fullScreen = 0
windowX = 1020
windowY = 720
banner="resources/banner.png"
backgroundColour = "#E3D2B4"

global displayCentre

class Main(wx.Frame):
	"""make a frame, inherits wx.Frame"""
	def __init__(self):					 
		# create a frame, no parent, default to wxID_ANY
		if fullScreen:
			wx.Frame.__init__(self, None, wx.ID_ANY, 'Full display size', pos=(0, 0), size=wx.DisplaySize())
			self.ShowFullScreen(True)
			imageLeft = wx.DisplaySize()[0] - 1020
		else:
			wx.Frame.__init__(self, None, wx.ID_ANY, 'wxButton', pos=(0,0), size=(windowX, windowY),
				style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
					wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
			imageLeft = 0
			
		self.ClearBackground()
		self.SetBackgroundColour(backgroundColour)
		
		wximg = wx.Image(banner) # Load background image
		wxbanner=wximg.ConvertToBitmap() # convert to a bit map
		wx.StaticBitmap(self,-1,wxbanner,((imageLeft/2),0))  # write the bitmap to self
		self.SetTitle(programName+" ("+programVersion+")")
		self.Show(True)
		
		displayCentre = int((windowX)/2)
		
		#label1
		font1 = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')		
	
		self.st1 = wx.StaticText(self, -1, "Search:", pos=(displayCentre-490, 192))
		self.st1.SetFont(font1)
		self.st1.SetForegroundColour('black')
		
		#search text entry
		entryfont = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
		self.search = wx.TextCtrl(self, -1, "", size=(400, 50), pos=(displayCentre-350, 188), style=wx.TE_PROCESS_ENTER)
		self.search.SetFont(entryfont)
		#self.search.Bind(wx.EVT_TEXT_ENTER, self.b1Click)
		self.search.SetFocus()
		
		self.searchb = wx.Button(self, id=-1, label='Search',
    	    pos=(displayCentre+300, 184), size=(180, 60))
		#self.searchb.Bind(wx.EVT_BUTTON, self.b1Click)
		# optional tooltip
		self.searchb.SetToolTip(wx.ToolTip("Search for a record"))
		
		self.register = wx.Button(self, id=-1, label='Register',
			pos=(displayCentre+300, 249), size=(180, 60))
		#self.register.Bind(wx.EVT_BUTTON, self.button3Click)
		# optional tooltip
		self.register.SetToolTip(wx.ToolTip("Register a new record (complete)"))
		
		self.searchb = wx.Button(self, id=-1, label='Visitor',
			pos=(displayCentre+300, 314), size=(180, 60))
		#self.searchb.Bind(wx.EVT_BUTTON, self.button3Click)
		self.searchb.SetToolTip(wx.ToolTip("Prints a name tag without entering into the permanent database"))
		
		self.searchb = wx.Button(self, id=-1, label='Last Search', pos=(displayCentre+300, 379), size=(180, 60))
		#self.searchb.Bind(wx.EVT_BUTTON, self.button3Click)
		# optional tooltip
		self.searchb.SetToolTip(wx.ToolTip("Register a new entry"))
		
		self.stat = wx.Button(self, id=-1, label='View/Print Report', pos=(displayCentre-480, 314), size=(260, 60))
	
		self.exitb = wx.Button(self, id=-1, label='Exit',	pos=(displayCentre-210, 314), size=(260, 60))
		self.exitb.Bind(wx.EVT_BUTTON, self.close)
		
		self.config = wx.Button(self, id=-1, label='Configuration', pos=(displayCentre-480, 379), size=(260, 60))
		
		self.service = wx.Button(self, id=-1, label='Lock screen', pos=(displayCentre-210, 379), size=(260, 60))		
				
		self.b1 = wx.Button(self, id=-1, label='1',  pos=(displayCentre+90, 184), size=(60, 60))	
		self.b2 = wx.Button(self, id=-1, label='2', pos=(displayCentre+155, 184), size=(60, 60))
		self.b3 = wx.Button(self, id=-1, label='3', pos=(displayCentre+220, 184), size=(60, 60))
			
		self.b4 = wx.Button(self, id=-1, label='4', pos=(displayCentre+90, 249), size=(60, 60))	
		self.b5 = wx.Button(self, id=-1, label='5', pos=(displayCentre+155, 249), size=(60, 60))
		self.b6 = wx.Button(self, id=-1, label='6', pos=(displayCentre+220, 249), size=(60, 60))
			
		self.b7 = wx.Button(self, id=-1, label='7', pos=(displayCentre+90, 314), size=(60, 60))	
		self.b8 = wx.Button(self, id=-1, label='8', pos=(displayCentre+155, 314), size=(60, 60))
		self.b9 = wx.Button(self, id=-1, label='9', pos=(displayCentre+220, 314), size=(60, 60))
			
		self.bAll = wx.Button(self, id=-1, label='All',  pos=(displayCentre+90, 379), size=(60, 60))	
		self.b0 = wx.Button(self, id=-1, label='0',     pos=(displayCentre+155, 379), size=(60, 60))
		self.bClr = wx.Button(self, id=-1, label='Clr', pos=(displayCentre+220, 379), size=(60, 60))
		
		#bindings:
		self.b1.Bind(wx.EVT_BUTTON, self.b1Click)
		self.b2.Bind(wx.EVT_BUTTON, self.b2Click)
		self.b3.Bind(wx.EVT_BUTTON, self.b3Click)
		self.b4.Bind(wx.EVT_BUTTON, self.b4Click)
		self.b5.Bind(wx.EVT_BUTTON, self.b5Click)
		self.b6.Bind(wx.EVT_BUTTON, self.b6Click)
		self.b7.Bind(wx.EVT_BUTTON, self.b7Click)
		self.b8.Bind(wx.EVT_BUTTON, self.b8Click)
		self.b9.Bind(wx.EVT_BUTTON, self.b9Click)
		self.b0.Bind(wx.EVT_BUTTON, self.b0Click)
		self.bAll.Bind(wx.EVT_BUTTON, self.bAllClick)
		self.bClr.Bind(wx.EVT_BUTTON, self.bClrClick)

		self.SetDefaultItem(self.searchb)
		self.Show(True)
		
	#functions
	def close(self, event):
		self.Close()
		application.ExitMainLoop()
		
	def b1Click(self, event):
		
		
		
application = wx.PySimpleApp()
# call class MyFrame
window = Main()
#window2 = Search()
# start the event loop
application.MainLoop()

#exit after main loop
exit()
