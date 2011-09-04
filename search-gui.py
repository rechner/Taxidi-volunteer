#!/usr/bin/env python
#-*- coding:utf-8 -*-

# this is just for testing with. This window will eventually be merged with the menu source,
# either by hiding the menu elements (YES!) or via a new class (new window) [meh].

import wx

programName = "Taxidi"  #python does not care what type a variable is. No more var$ <> var.
programVersion = "0.0.1b"
fullScreen = 1
windowX = 1020
windowY = 720
banner="resources/banner.png"

class Search(wx.Frame):
	"""make a frame, inherits wx.Frame""" # < triple quoted strings can also be used]
	def __init__(self):
	
		if fullScreen:
			wx.Frame.__init__(self, None, wx.ID_ANY, 'Full display size', pos=(0, 0), size=wx.DisplaySize())
		else:
			wx.Frame.__init__(self, None, wx.ID_ANY, 'wxButton', pos=(0,0), size=(windowX, windowY),
					style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
		
		self.SetBackgroundColour("#E3D2B4") 
		self.ClearBackground()
		imageLeft = self.GetClientSize()[0] - 1020
		
		wximg = wx.Image(banner) # Load background image
		#wximg.Rescale(self.GetClientSize()[0], self.GetClientSize()[1])) # rescale to fit screen
		wximg.Resize(self.GetClientSize(), (imageLeft/2, 0))
		wxbanner=wximg.ConvertToBitmap() # convert to a bit map
		wx.StaticBitmap(self,-1,wxbanner,(wximg.GetWidth()-1020,0))  # write the bitmap to self
		self.SetTitle(programName+" ("+programVersion+")")
		self.Show(True)
	
		displayCenter = int((self.GetClientSize()[0])/2)
		
		#label1
		font1 = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')		
	
		self.st1 = wx.StaticText(self, -1, "Search:", pos=(displayCenter-490, 192))
		self.st1.SetFont(font1)
		self.st1.SetForegroundColour('black')
		
		#search text entry
		entryfont = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
		self.search = wx.TextCtrl(self, -1, "", size=(400, 50), pos=(displayCenter-350, 188), style=wx.TE_PROCESS_ENTER)
		self.search.SetFont(entryfont)
		self.search.Bind(wx.EVT_TEXT_ENTER, self.b1Click)
		self.search.SetFocus()
		
		self.searchb = wx.Button(self, id=-1, label='Search',
    	    pos=(displayCenter+300, 184), size=(180, 60))
		self.searchb.Bind(wx.EVT_BUTTON, self.b1Click)
		# optional tooltip
		self.searchb.SetToolTip(wx.ToolTip("Search for a record"))
		
		self.register = wx.Button(self, id=-1, label='Register',
			pos=(displayCenter+300, 249), size=(180, 60))
		#self.register.Bind(wx.EVT_BUTTON, self.button3Click)
		# optional tooltip
		self.register.SetToolTip(wx.ToolTip("Register a new record (complete)"))
		
		self.searchb = wx.Button(self, id=-1, label='Visitor',
			pos=(displayCenter+300, 314), size=(180, 60))
		#self.searchb.Bind(wx.EVT_BUTTON, self.button3Click)
		self.searchb.SetToolTip(wx.ToolTip("Prints a name tag without entering into the permanent database"))
		
		self.searchb = wx.Button(self, id=-1, label='Last Search', pos=(displayCenter+300, 379), size=(180, 60))
		#self.searchb.Bind(wx.EVT_BUTTON, self.button3Click)
		# optional tooltip
		self.searchb.SetToolTip(wx.ToolTip("Register a new entry"))
		
		self.stat = wx.Button(self, id=-1, label='Current Statistics', pos=(displayCenter-480, 314), size=(245, 60))
		
	
		self.exitb = wx.Button(self, id=-1, label='Exit',	pos=(displayCenter-200, 314), size=(245, 60))
		self.exitb.Bind(wx.EVT_BUTTON, self.close)
		
				
		self.b1 = wx.Button(self, id=-1, label='1',  pos=(displayCenter+90, 184), size=(60, 60))	
		self.b1.Bind(wx.EVT_BUTTON, self.b1Click)
		self.b2 = wx.Button(self, id=-1, label='2', pos=(displayCenter+155, 184), size=(60, 60))
		self.b3 = wx.Button(self, id=-1, label='3', pos=(displayCenter+220, 184), size=(60, 60))
			
		self.b1 = wx.Button(self, id=-1, label='4', pos=(displayCenter+90, 249), size=(60, 60))	
		self.b2 = wx.Button(self, id=-1, label='5', pos=(displayCenter+155, 249), size=(60, 60))
		self.b3 = wx.Button(self, id=-1, label='6', pos=(displayCenter+220, 249), size=(60, 60))
			
		self.b1 = wx.Button(self, id=-1, label='7', pos=(displayCenter+90, 314), size=(60, 60))	
		self.b2 = wx.Button(self, id=-1, label='8', pos=(displayCenter+155, 314), size=(60, 60))
		self.b3 = wx.Button(self, id=-1, label='9', pos=(displayCenter+220, 314), size=(60, 60))
			
		self.b1 = wx.Button(self, id=-1, label='All',  pos=(displayCenter+90, 379), size=(60, 60))	
		self.b2 = wx.Button(self, id=-1, label='0',     pos=(displayCenter+155, 379), size=(60, 60))
		self.b3 = wx.Button(self, id=-1, label='Clr', pos=(displayCenter+220, 379), size=(60, 60))
		
		#bindings:
		self.b1.Bind(wx.EVT_BUTTON, self.b1Click)

		self.SetDefaultItem(self.searchb)

		# show the frame
		self.Show(True)
		
#functions should be in first most block for the window class
	def b1Click(self, event):
		print "1"

	def close(self, event):
		self.Close()
		application.ExitMainLoop()

application = wx.PySimpleApp()
# call class MyFrame
window = Search()
# start the event loop
application.MainLoop()
