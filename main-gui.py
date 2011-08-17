#!/usr/bin/env python
#-*- coding:utf-8 -*-

# These two headers are important in any type of script, because they tell the system
# what interpreter to use if the script is called from the shell. (i.e. ./file.py).
# Even though comments prevent lines of code from being executed, they are still read
# by the shell. This always starts with #! and points to the full path of an interpreter.
# this is usually referred to as the "crunch bang" line. The second line tells python
# what kind of character set to expect, as various encodings are available on different
# systems. The ISO standard, along with what is used primarily in UNIX systems is utf-8
# or Unicode. Windows likes to use ISO 8859-15, also called western encoding. The first
# line must be the first in every script that can be called from the system shell, and
# can not include any white space before it. Of course if it is called using python, 
# this line is irrelevant.

# Python has the ability to use special libraries referred to as modules. Modules can
# be included in a program by using the import directive.

import wx
import os

# Alternatively, you can import only portions of modules, which is often favored as it
# consumes less memory. An alternative to the above line is: 

#from wx import *

# The wx or wXWindow library is a nice tool kit for creating GUIs. There are several
# others such as tkinter, which is popular for being cross platform, although nearly
# all python modules and scripts are portable, except for those which use platform
# specific coding, such as a scripts that use directories to load and save files.
# (Try opening C:\blah.txt on a UNIX platform). I'm not completely sure, but I think
# that wxwindows is cross platform so it'll work perfectly for Taxídí. If not then
# We'll have to use tkinter. I like wx better because it renders perfectly with 
# themes in Linux, where as tk takes you back to the days of TWM. 

programName = "Taxidi"  #python does not care what type a variable is. No more var$ <> var.
programVersion = "0.0.1b"
fullScreen = 0
windowX = 1020
windowY = 720
banner="resources/banner.png"

class Main(wx.Frame):
	"""make a frame, inherits wx.Frame""" # < triple quoted strings can also be used 
	def __init__(self):					  # for quotes.
		# create a frame, no parent, default to wxID_ANY
		if fullScreen:
			wx.Frame.__init__(self, None, wx.ID_ANY, 'Full display size', pos=(0, 0), size=wx.DisplaySize())
		else:
			wx.Frame.__init__(self, None, wx.ID_ANY, 'wxButton', pos=(0,0), size=(windowX, windowY),
				style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
					wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
			
		self.SetBackgroundColour("black") 
		self.ClearBackground()
		imageLeft = self.GetClientSize()[0] - 1020
		
		global displayCenter
		displayCenter = int((self.GetClientSize()[0])/2)
		
		wximg = wx.Image(banner) # Load background image
		#wximg.Rescale(self.GetClientSize()[0], self.GetClientSize()[1])) # rescale to fit screen
		#wximg.Resize(self.GetClientSize(), (imageLeft/2, 0))
		wxbanner=wximg.ConvertToBitmap() # convert to a bit map
		wx.StaticBitmap(self,-1,wxbanner,(imageLeft,0))  # write the bitmap to self
		self.SetTitle(programName+" ("+programVersion+")")
		self.Show(True)
		
		
		
		#wx.MessageBox(str(wx.DisplaySize()[0]), 'Info')  
		#main menu buttons:  buttonStart, buttonKiosk, buttonManage, buttonConfigure, buttonAbout, buttonQuit
		
		self.buttonStart = wx.Button(self, id=-1, label='Begin Check-in',
			pos=(displayCenter-330, 168), size=(275, 50))
		self.buttonStart.Bind(wx.EVT_BUTTON, self.startClick)
		self.buttonStart.SetToolTip(wx.ToolTip("Start normal check-in routine."))

		self.buttonKiosk = wx.Button(self, id=-1, label='Kiosk Mode',
			pos=(displayCenter+10, 168), size=(275, 50))
		self.buttonKiosk.Bind(wx.EVT_BUTTON, self.button2Click)
		self.buttonKiosk.SetToolTip(wx.ToolTip("Start in kiosk / automated check-in mode"))

		self.buttonConfigure = wx.Button(self, id=-1, label='Configure',
			pos=(displayCenter-330, 228), size=(275, 50))
		self.buttonConfigure.Bind(wx.EVT_BUTTON, self.button3Click)
		self.buttonConfigure.SetToolTip(wx.ToolTip("Set options and settings."))

		self.buttonAbout = wx.Button(self, id=-1, label='About',
			pos=(displayCenter+10, 228), size=(275, 50))
		self.buttonAbout.Bind(wx.EVT_BUTTON, self.OnAboutBox)
		self.buttonAbout.SetToolTip(wx.ToolTip("Set options and preferences"))

		self.buttonServices = wx.Button(self, id=-1, label='Manage Services',
			pos=(displayCenter-330, 288), size=(275, 50))
		self.buttonServices.Bind(wx.EVT_BUTTON, self.button5Click)
		self.buttonServices.SetToolTip(wx.ToolTip("Manage services, and set start times."))

		self.buttonActivities = wx.Button(self, id=-1, label='Manage Activites',
			pos=(displayCenter+10, 288), size=(275, 50))
		self.buttonActivities.Bind(wx.EVT_BUTTON, self.quit)
		self.buttonActivities.SetToolTip(wx.ToolTip("Manage activites and nametag graphics"))
		
		self.buttonQuit = wx.Button(self, id=-1, label="Quit",
			pos=(displayCenter-330, 348), size=(615, 50))
		self.buttonQuit.Bind(wx.EVT_BUTTON, self.quit)
		
	
	
		#label1
		font1 = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')		
	
		self.st1 = wx.StaticText(self, -1, "Search:", pos=(displayCenter-490, 192))
		self.st1.SetFont(font1)
		self.st1.SetForegroundColour('white')
		self.st1.Hide()
		
		#search text entry
		entryfont = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
		self.search = wx.TextCtrl(self, -1, "", size=(400, 50), 
			pos=(displayCenter-350, 188), style=wx.TE_PROCESS_ENTER)
		self.search.SetFont(entryfont)
		self.search.Bind(wx.EVT_TEXT_ENTER, searchRecord)
		self.search.Hide()
		
		self.searchb = wx.Button(self, id=-1, label='Search', pos=(displayCenter+300, 184), size=(180, 60))
		self.searchb.Bind(wx.EVT_BUTTON, searchRecord)
		# optional tooltip
		self.searchb.SetToolTip(wx.ToolTip("Search for a record"))
		self.searchb.Hide()

		self.buttonRegister = wx.Button(self, id=-1, label='Register',
			pos=(displayCenter+300, 249), size=(180, 60))
		#self.searchb.Bind(wx.EVT_BUTTON, self.button3Click)
		# optional tooltip
		self.buttonRegister.SetToolTip(wx.ToolTip("Register a new record (complete)"))
		self.buttonRegister.Hide()
		
		self.buttonVisitor = wx.Button(self, id=-1, label='Visitor',
			pos=(displayCenter+300, 314), size=(180, 60))
		#self.searchb.Bind(wx.EVT_BUTTON, self.button3Click)
		self.buttonVisitor.SetToolTip(wx.ToolTip("Prints a name tag without entering into the permanent database"))
		self.buttonVisitor.Hide()
		
		self.buttonLast = wx.Button(self, id=-1, label='Last Search', pos=(displayCenter+300, 379), size=(180, 60))
		#self.searchb.Bind(wx.EVT_BUTTON, self.button3Click)
		# optional tooltip
		self.buttonLast.SetToolTip(wx.ToolTip("Register a new entry"))
		self.buttonLast.Hide()
	
		self.buttonExit = wx.Button(self, id=-1, label='Exit',	pos=(displayCenter-200, 379), size=(180, 60))
		self.buttonExit.Bind(wx.EVT_BUTTON, self.exitSearch)
		self.buttonExit.SetToolTip(wx.ToolTip("Prints a name tag without entering into the permanent database"))
		self.buttonExit.Hide()
		
		
		self.b1 = wx.Button(self, id=-1, label='1',  pos=(displayCenter+90, 184), size=(60, 60))	
		self.b1.Bind(wx.EVT_BUTTON, b1Click)
		self.b2 = wx.Button(self, id=-1, label='2', pos=(displayCenter+155, 184), size=(60, 60))
		self.b3 = wx.Button(self, id=-1, label='3', pos=(displayCenter+220, 184), size=(60, 60))
		self.b1.Hide()
		self.b2.Hide()
		self.b3.Hide()
			
		self.b4 = wx.Button(self, id=-1, label='4', pos=(displayCenter+90, 249), size=(60, 60))	
		self.b5 = wx.Button(self, id=-1, label='5', pos=(displayCenter+155, 249), size=(60, 60))
		self.b6 = wx.Button(self, id=-1, label='6', pos=(displayCenter+220, 249), size=(60, 60))
		self.b4.Hide()
		self.b5.Hide()
		self.b6.Hide()
		
		self.b7 = wx.Button(self, id=-1, label='7', pos=(displayCenter+90, 314), size=(60, 60))	
		self.b8 = wx.Button(self, id=-1, label='8', pos=(displayCenter+155, 314), size=(60, 60))
		self.b9 = wx.Button(self, id=-1, label='9', pos=(displayCenter+220, 314), size=(60, 60))
		self.b7.Hide()
		self.b8.Hide()
		self.b9.Hide()
			
		self.bAll = wx.Button(self, id=-1, label='All',  pos=(displayCenter+90, 379), size=(60, 60))	
		self.b0 = wx.Button(self, id=-1, label='0',     pos=(displayCenter+155, 379), size=(60, 60))
		self.bClr = wx.Button(self, id=-1, label='Clr', pos=(displayCenter+220, 379), size=(60, 60))
		
		self.bAll.Hide()
		self.b0.Hide()
		self.bClr.Hide()
		
		

		# show the frame
		self.Show(True)

	def startClick(self,event):
		start()
		#self.button1.Hide()
		#self.button2.Show()

	def button2Click(self,event):
		#self.button2.Hide()
		self.SetTitle("Button2 clicked")
		#self.button1.Show()

	def button3Click(self,event):
		#self.button3.Disable()
		self.SetTitle("Button3 clicked")
		#self.button4.Enable()

	def button4Click(self,event):
		#self.button4.Disable()
		self.SetTitle("Button4 clicked")
		#self.button3.Enable()
		
	def button5Click(self,event):
		self.SetTitle("Button5 clicked")
		
	def exitSearch(self,event):
		window.SetTitle(programName+" ("+programVersion+")")
		searchHide()
		menuShow()
	
	def OnAboutBox(self, event):
		description = """Taxídí is an advanced check-in system for nurseries, 
churches, and classes. It can be used to track attendance 
or at events where attendance must be tracked.

Taxidi was written by Zac Sturgeon and Britt McGlamry for
Journey Church in Millbrook, Alabama.
"""

		licence = """Taxidi is the intellectual property of JKL Technologies, Incorporated. All rights reserved."""
		
		info = wx.AboutDialogInfo()
		
		info.SetIcon(wx.Icon('resources/taxidi.png', wx.BITMAP_TYPE_PNG))
		info.SetName('Taxídí')
		info.SetVersion('0.02-preview')
		info.SetDescription(description)
		info.SetCopyright('© 2010 JKL Tech, Inc')
		info.SetWebSite('http://jkltechinc.homeunix.net/taxidi')
		info.SetLicence(licence)
		info.AddDeveloper('Zac Sturgeon')
		info.AddDocWriter('Britt McGlamry')
		info.AddArtist('Zac Sturgeon')
		
		#info.AddTranslator('')
		wx.AboutBox(info)

	
	def quit(self,event):
		self.Close()
		application.ExitMainLoop()
	
def start():
    window.SetTitle("Taxidi: Check-in Started")
    menuHide()
    searchShow()	

def menuHide():
	window.buttonStart.Hide()
	window.buttonKiosk.Hide()
	window.buttonManage.Hide()
	window.buttonConfigure.Hide()
	window.buttonAbout.Hide()
	window.buttonQuit.Hide()
	
def menuShow():
	window.buttonStart.Show()
	window.buttonKiosk.Show()
	window.buttonManage.Show()
	window.buttonConfigure.Show()
	window.buttonAbout.Show()
	window.buttonQuit.Show()

def b1Click(event):
	print "hello world"
	pass

def searchShow():
	window.b1.Show()
	window.b2.Show()
	window.b3.Show()
	window.b4.Show()
	window.b5.Show()
	window.b6.Show()
	window.b7.Show()
	window.b8.Show()
	window.b9.Show()
	window.bClr.Show()
	window.b0.Show()
	window.bAll.Show()
	window.search.Show()
	window.st1.Show()
	window.searchb.Show()
	window.buttonVisitor.Show()
	window.buttonRegister.Show()
	window.buttonLast.Show()
	window.buttonExit.Show()	
	window.search.SetFocus()
	#easiest way to play sounds, forks to background using shell.
	os.system("aplay resources/ready.wav &")   #(requires alsa-utils)
	
def searchHide():
	window.b1.Hide()
	window.b2.Hide()
	window.b3.Hide()
	window.b4.Hide()
	window.b5.Hide()
	window.b6.Hide()
	window.b7.Hide()
	window.b8.Hide()
	window.b9.Hide()
	window.bClr.Hide()
	window.b0.Hide()
	window.bAll.Hide()
	window.search.Hide()
	window.st1.Hide()
	window.searchb.Hide()
	window.buttonVisitor.Hide()
	window.buttonRegister.Hide()
	window.buttonLast.Hide()
	window.buttonExit.Hide()
    
def searchRecord(event):
	if event:
		wx.MessageBox(window.search.GetValue(), 'Info')
		window.search.SetValue("")
	

application = wx.PySimpleApp()
# call class MyFrame
window = Main()
#window2 = Search()
# start the event loop
application.MainLoop()

#exit after main loop
exit()
