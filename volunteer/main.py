#!/usr/bin/env python
#-*- coding:utf-8 -*-

#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.


# Notes:
# Perhaps each "page" should be organized into separate classes?
# Full screen was broken when panel was added.  Style problem?
# (Panel needed for tab-traversal. Perhaps we can 'full screen' it
# 	just by calling it in X11 with no WM and size=Wx.DisplaySize() )

#TODO Future:
# - Add reports which tally each service and ministry.
#	i.e. First service: 21 volunteers total
#		 Second service: 32 volunteers total, etc.
# - Add ability to edit/delete records.

import wx
from wx.lib.masked import TextCtrl as maskedTextCtrl
import conf
import datetime
import volunteerSQL as sql
import csv
import files
import mail
import pynotify

pynotify.init("Dream Team Check-in")

def as_bool(inp):
	if inp == 'True':
		inp = True
	else:
		inp = False
	return inp

config = conf.get()

#config values
programName = 'Journey Volunteer Check-in'
programVersion = '0.10.0'
fullScreen = as_bool(config['fullScreen'])
windowX = int(config['windowX'])
windowY = int(config['windowY'])
banner = config['banner']
backgroundColour = config['backgroundColour']

#ADD TO CONFIG:
services = ['First Servce', 'Second Service', 'Third Service']
ministries = [u'Café', 'Parking', 'Explorers', 'Explorers Check-in',
	'Outfitters', 'Outfitters Check-in', 'Usher', 'Tech Team', 
	'Route 56 ', 'Greeter']
selectedServices = []
selectedMinistries = []
global logFile
logFile = 'database/report.csv'
archiveFolder = 'database/archive/'  #MUST Have trailing slash


#open log file, read first row's date column, and compare it to today.
#if it is older, then rename the file to reflect the date.

try:
	f = open(logFile, 'rb')
	f.close()
except IOError:
	f = open(logFile, 'w')
	f.write('"ID","Name","Services served","Ministries served","Date","Time"\n')
	f.close()
f = open(logFile, 'rb')
reader = csv.reader(f)
readerTmp = []
for row in reader:
	readerTmp.append(row)
f.close()
print "Debug: latest write to CSV was '" + readerTmp[0][4]+"'"
if readerTmp[0][4] != datetime.datetime.now().strftime("%a %d %B, %Y") and readerTmp[0][4] != 'Date':
	#copy to archive file and clear the old file.
	print "Debug: lastest write older than today; archiving data."
	files.copy(logFile, archiveFolder+
		datetime.datetime.now().strftime("%Y-%m-%d.csv"))
	f = open(logFile, 'w')
	f.write('"ID","Name","Services served","Ministries served","Date","Time"\n')
	f.close()
	print "Debug: CSV data reset."


global database
database = 'database/users.db'

handler = sql.Database(database)

global displayCentre
global resultList
global querySelection
resultList = []

class Main(wx.Frame):
	"""make a frame, inherits wx.Frame"""
	def __init__(self):					 
		# create a frame, no parent, default to wxID_ANY
		if fullScreen:
			wx.Frame.__init__(self, None, wx.ID_ANY, 'Full display size',
				pos=(0, 0), size=wx.DisplaySize())
			#self.ShowFullScreen(True)
			imageLeft = wx.DisplaySize()[0] - 1020
		else:
			wx.Frame.__init__(self, None, wx.ID_ANY, 'Taxidi', 
				pos=(0,0), size=(windowX, windowY),
				style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
				wx.CAPTION|wx.CLOSE_BOX|wx.TAB_TRAVERSAL|wx.WANTS_CHARS)
				
			imageLeft = 0
			
		self.panel = wx.Panel(self, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL) 
		self.ClearBackground()
		self.SetBackgroundColour(backgroundColour)
		wximg = wx.Image(banner) # Load background image
		wxbanner=wximg.ConvertToBitmap() # convert to a bit map
		wx.StaticBitmap(self.panel,-1,wxbanner,((imageLeft/2),0))  # write the bitmap to self
		
		self.SetTitle(programName+" ("+programVersion+")")
		self.Show(True)
		wx.EVT_CLOSE(self, self.OnQuit)
		
		displayCentre = int((self.GetClientSize()[0])/2)
		
		#label1
		font1 = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')		
		font2 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
		font3 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False, u'Arial')
	
		self.st1 = wx.StaticText(self.panel, -1, "Search:", pos=(displayCentre-490, 192))
		self.st1.SetFont(font1)
		self.st1.SetForegroundColour('black')
		
		self.statusText = wx.StaticText(self.panel, -1, """Ready: To begin, search by name, last four 
digits of phone number, or scan barcode.""",
			pos=(displayCentre - 475, 250))
		self.statusText.SetFont(font2)
		self.statusText.SetForegroundColour('dark green')
		
		#search text entry
		entryfont = wx.Font(24, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
		self.search = wx.TextCtrl(self.panel, -1, "", size=(400, 50), pos=(displayCentre-350, 188), style=wx.TE_PROCESS_ENTER)
		self.search.SetFont(entryfont)
		self.search.Bind(wx.EVT_TEXT_ENTER, self.query)
		self.search.SetFocus()
		
		self.searchb = wx.Button(self.panel, id=-1, label='Search',
			pos=(displayCentre+300, 184), size=(180, 60))
		self.searchb.Bind(wx.EVT_BUTTON, self.query)
		self.searchb.SetToolTip(wx.ToolTip("Search for a record"))
		
		self.register = wx.Button(self.panel, id=-1, label='Register',
			pos=(displayCentre+300, 249), size=(180, 60))
		self.register.Bind(wx.EVT_BUTTON, self.Register)
		self.register.SetToolTip(wx.ToolTip("Register a new record (complete)"))
		
		self.lastb = wx.Button(self.panel, id=-1, label='Last Search', 
			pos=(displayCentre+300, 314), size=(180, 60))
			
		self.about = wx.Button(self.panel, id=-1, label='About',
			pos=(displayCentre+300, 379), size=(180, 60)) 
		self.about.Bind(wx.EVT_BUTTON, self.aboutTaxidi)
				
		self.stat = wx.Button(self.panel, id=-1, 
			label='Email Report', pos=(displayCentre-480, 379), 
			size=(260, 60))
		self.stat.Bind(wx.EVT_BUTTON, self.report)
	
		self.exitb = wx.Button(self.panel, id=-1, label='Exit',	
			pos=(displayCentre-210, 379), size=(260, 60))
		self.exitb.Bind(wx.EVT_BUTTON, self.close)
		
		#self.config = wx.Button(self.panel, id=-1, 
			#label='Configuration', pos=(displayCentre-480, 314), 
			#size=(260, 60))
		
		#self.lock = wx.Button(self.panel, id=-1, label='Lock screen', 
			#pos=(displayCentre-210, 379), size=(260, 60))	
		
				
		self.b1 = wx.Button(self.panel, id=-1, label='1',  pos=(displayCentre+90, 184), size=(60, 60))	
		self.b2 = wx.Button(self.panel, id=-1, label='2', pos=(displayCentre+155, 184), size=(60, 60))
		self.b3 = wx.Button(self.panel, id=-1, label='3', pos=(displayCentre+220, 184), size=(60, 60))
		self.b4 = wx.Button(self.panel, id=-1, label='4', pos=(displayCentre+90, 249), size=(60, 60))	
		self.b5 = wx.Button(self.panel, id=-1, label='5', pos=(displayCentre+155, 249), size=(60, 60))
		self.b6 = wx.Button(self.panel, id=-1, label='6', pos=(displayCentre+220, 249), size=(60, 60))
		self.b7 = wx.Button(self.panel, id=-1, label='7', pos=(displayCentre+90, 314), size=(60, 60))	
		self.b8 = wx.Button(self.panel, id=-1, label='8', pos=(displayCentre+155, 314), size=(60, 60))
		self.b9 = wx.Button(self.panel, id=-1, label='9', pos=(displayCentre+220, 314), size=(60, 60))
		self.bAll = wx.Button(self.panel, id=-1, label='All',  pos=(displayCentre+90, 379), size=(60, 60))	
		self.b0 = wx.Button(self.panel, id=-1, label='0',	 pos=(displayCentre+155, 379), size=(60, 60))
		self.bClr = wx.Button(self.panel, id=-1, label='Clr', pos=(displayCentre+220, 379), size=(60, 60))
		
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
		
		
		#setup search results page
		self.st2 = wx.StaticText(self.panel, -1, 
			"Search Results. Please highlight your name and press 'Forward'",
			pos=(displayCentre-490, 147))
		self.st2.SetFont(font1)
		self.st2.SetForegroundColour('black')
		
		self.listBox = wx.ListBox(self.panel, id=-1,
			pos=(displayCentre-490, 190), size=(968, 402), style=wx.LB_EXTENDED)
		self.listBox.SetFont(entryfont)
		
		self.next1b = wx.Button(self.panel, wx.ID_FORWARD,
			pos=(displayCentre+300, 610), size=(180, 60))
		self.next1b.Bind(wx.EVT_BUTTON, self.selectServices)
		
		self.back1b = wx.Button(self.panel, wx.ID_BACKWARD,
			pos=(displayCentre+100, 610), size=(180, 60))
		self.back1b.Bind(wx.EVT_BUTTON, self.backToSearch)
		
		self.deleteb = wx.Button(self.panel, wx.ID_DELETE,
			pos=(displayCentre-490, 610), size=(180, 60))
		self.deleteb.Bind(wx.EVT_BUTTON, self.deleteSelected)
		 
	
				
		#select services page
		# recycle the statictext (st2)
		# we only need unique buttons.
		
		self.serviceButtons = []  #save the buttons in a list
		posX = 0
		
		for i in range(0,len(services)):
			posY = displayCentre-460
			posX = 210+(i*70)
			if i > 4 and i < 10:
				posY = displayCentre-150
				posX = 190+((i-5)*70)
			if i >= 10:
				posY = displayCentre+160
				posX = 210+((i-10)*70)
			self.serviceButtons.append(wx.ToggleButton(self.panel,
				id=-1, label=services[i], pos=(posY, posX), 
				size=(280, 60)))
			self.serviceButtons[i].Bind(wx.EVT_TOGGLEBUTTON, lambda evt, 
				temp=i: self.toggleService(evt, temp), id=-1)
			
				
		self.next2b = wx.Button(self.panel, wx.ID_FORWARD,
			pos=(displayCentre+300, 610), size=(180, 60))
		self.next2b.Bind(wx.EVT_BUTTON, self.selectMinistry)
		self.next2b.Disable()
		
		self.back2b = wx.Button(self.panel, wx.ID_BACKWARD,
			pos=(displayCentre+100, 610), size=(180, 60))
		self.back2b.Bind(wx.EVT_BUTTON, self.backToResults)
		
		
		#select ministry
		self.ministryButtons = []
		posX = 0
		posY = 0
		
		for i in range(0, len(ministries)):
			posX = displayCentre-460
			posY = 210+(i*70)
			if i > 4 and i < 10:
				posX = displayCentre-150
				posY = 210+((i-5)*70)
			if i >= 10:
				posX = displayCentre+160
				posY = 210+((i-10)*70)
			self.ministryButtons.append(wx.ToggleButton(self.panel,
				id=-1, label=ministries[i], pos=(posX, posY),
				size=(280, 60)))
			self.ministryButtons[i].Bind(wx.EVT_TOGGLEBUTTON, lambda evt,
				temp=i: self.toggleMinistry(evt, temp), id=-1)
				
		self.next3b = wx.Button(self.panel, wx.ID_FORWARD,
			pos=(displayCentre+300, 610), size=(180, 60))
		self.next3b.Bind(wx.EVT_BUTTON, self.finalReview)
		self.next3b.Disable()
		
		self.back3b = wx.Button(self.panel, wx.ID_BACKWARD,
			pos=(displayCentre+100, 610), size=(180, 60))
		self.back3b.Bind(wx.EVT_BUTTON, self.backToServices)
		
		#final reveiw page
		self.reviewText = wx.StaticText(self.panel, -1, "", 
			pos=((displayCentre-460), 250))
		self.reviewText.SetFont(font3)
		
		self.next4b = wx.Button(self.panel, id=-1, label='Finish and Submit',
			pos=(displayCentre+300, 610), size=(180, 60))
		self.next4b.Bind(wx.EVT_BUTTON, self.submit)
		
		self.back4b = wx.Button(self.panel, wx.ID_BACKWARD,
			pos=(displayCentre+100, 610), size=(180, 60))
		self.back4b.Bind(wx.EVT_BUTTON, self.backToMinistries)
		
		
		#register		
		self.registerSt1 = wx.StaticText(self.panel, -1, "First:",
			pos=((displayCentre-450), 195))
		self.registerSt1.SetFont(entryfont)
		
		self.registerFirst = wx.TextCtrl(self.panel, -1, "", size=(320, 50), 
			pos=(displayCentre-370, 188))
		self.registerFirst.SetFont(entryfont)
		
		self.registerSt2 = wx.StaticText(self.panel, -1, "Last:",
			pos=((displayCentre-20), 195))
		self.registerSt2.SetFont(entryfont)
		
		self.registerLast = wx.TextCtrl(self.panel, -1, "", size=(320, 50),
			pos=((displayCentre+60), 188))
		self.registerLast.SetFont(entryfont)
		
		self.registerSt3 = wx.StaticText(self.panel, -1, "Phone:",
			pos=((displayCentre-450), 260))
		self.registerSt3.SetFont(entryfont)
		
		self.registerPhone = maskedTextCtrl(self.panel, -1, '', 
			mask = '(###) ###-####',
			size=(230, 50), pos=((displayCentre-340, 254)))
		self.registerPhone.SetFont(entryfont)
		
		self.registerSt4 = wx.StaticText(self.panel, -1, "Barcode:",
			pos=((displayCentre-80), 260))
		self.registerSt4.SetFont(entryfont)
		
		self.registerBarcode = wx.TextCtrl(self.panel, -1, '',
			size=(260, 50), pos=((displayCentre+60), 254))
		self.registerBarcode.SetFont(entryfont)
		
		self.registerBarcodeClear = wx.Button(self.panel, -1,
			'Clear', size=(50, 50), pos=((displayCentre+330), 254))
			
		self.registerAccept = wx.Button(self.panel, wx.ID_SAVE,
			size=(200, 60), pos=((displayCentre+210), 580))
		self.registerAccept.Bind(wx.EVT_BUTTON, self.registerSave)
			
		self.registerCancel = wx.Button(self.panel, wx.ID_CANCEL,
			size=(200, 60), pos=((displayCentre), 580))
		self.registerCancel.Bind(wx.EVT_BUTTON, self.registerCleanup)
		
		
		self.hideResult()
		self.hideServices()
		self.hideMinistries()
		self.hideFinish()
		self.hideRegister()
		
		

		
	#functions
	def close(self, event):
		dial = wx.MessageDialog(self, 
			"Do you really want exit?",
			"Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
		result = dial.ShowModal()
		dial.Destroy()
		if result == wx.ID_OK:
			self.Destroy()
			self.Close()
			application.ExitMainLoop()
		
	def b1Click(self, event):
		self.search.AppendText('1')
		self.search.SetFocus()
		
	def b2Click(self, event):
		self.search.AppendText('2')
		self.search.SetFocus()
		
	def b3Click(self, event):
		self.search.AppendText('3')
		self.search.SetFocus()
		
	def b4Click(self, event):
		self.search.AppendText('4')
		self.search.SetFocus()
		
	def b5Click(self, event):
		self.search.AppendText('5')
		self.search.SetFocus()
		
	def b6Click(self, event):
		self.search.AppendText('6')
		self.search.SetFocus()
		
	def b7Click(self, event):
		self.search.AppendText('7')
		self.search.SetFocus()
		
	def b8Click(self, event):
		self.search.AppendText('8')
		self.search.SetFocus()
		
	def b9Click(self, event):
		self.search.AppendText('9')
		self.search.SetFocus()
		
	def b0Click(self, event):
		self.search.AppendText('0')
		self.search.SetFocus()
		
	def bAllClick(self, event):
		self.search.SetValue('')
		self.query(self)
	
	def bClrClick(self, event):
		self.search.SetValue('')
		self.search.SetFocus()

		
	def query(self, event):
		global resultList #so other functions can access the list
		query = self.search.GetValue()
		resultList = self.query_test(query)
		if len(resultList) == 0:
			#display an error: No search results for '%s'
			self.statusText.SetLabel('No results for "%s"' % query)
			self.statusText.SetForegroundColour('dark red')
			self.notice('Error: No results for "%s"' % query)
			self.search.SelectAll()
			self.search.SetFocus()
			return 1
		
		for i in resultList:
			self.listBox.Append(i[1])
		
		self.hideSearch()
		self.showResult()
		self.listBox.Select(0)
		self.listBox.SetFocus()
		
	def query_test(self, query):
		global handler
		if query == '':
			res = handler.ReturnAll()
		else:
			try:
				query = int(query)
			except ValueError:
				query += "%"
			res = handler.Query(query)
		resultList = []
		for i in res:
			resultList.append([ i[0], i[1]+' '+i[2] ])
		return resultList
		
	def backToSearch(self, event):
		self.cleanupQuery()
		self.showSearch()
		self.hideResult()
		self.search.SetFocus()
		
	def selectServices(self, event):
		global querySelection
		self.hideResult()
		self.showServices()
		querySelection = self.listBox.GetSelections()[0]
		
	def deleteSelected(self, event):
		global querySelection
		global resultList
		global handler
		querySelection = self.listBox.GetSelections()[0]
		name = resultList[querySelection][1]
		dial = wx.MessageDialog(self, 
			"Do you really want to delete %s?" % name,
			"Confirm Delete", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
		result = dial.ShowModal()
		dial.Destroy()
		if result == wx.ID_OK:
			a=handler.Delete(resultList[querySelection][0])
			if a:
				self.notice('The user "%s" was successfully removed' % name)
			else:
				self.notice('An error has occured.  Unable to remove entry')
		#refresh the list
		resultList = []
		self.listBox.Clear()
		self.query(None)
	
		
	def backToServices(self, event):
		self.hideMinistries()
		self.showServices()
		
	def backToResults(self, event):
		self.hideServices()
		self.showResult()
		
	def selectMinistry(self, event):
		self.hideServices()
		self.showMinistries()
		
	def backToMinistries(self, event):
		self.hideFinish()
		self.showMinistries()
		
	def finalReview(self, event):  #compile all the information
		global resultList
		global querySelection
		global ministries
		global services
		global selectedServices
		global selectedMinistries
		selectedServices.sort()
		selectedMinistries.sort()
		servicesText = ''
		ministriesText = ''
		a = 0
		
		for i in selectedServices:
			a += 1  #counter
			#we use this to tell if we should add a comma to the list
			endTest = not(a == len(selectedServices))
			servicesText += services[i]+', '*endTest
		if len(selectedServices) == 1:
			servicesText = 'Service: '+servicesText
		else:
			servicesText = 'Services: '+servicesText
		a = 0	
		if len(selectedMinistries) == 1:
			ministriesText = 'Ministry: '+ministriesText
		else:
			ministriesText = 'Ministries: '+ministriesText
		for i in selectedMinistries:
			a += 1
			endTest = not(a == len(selectedMinistries))
			ministriesText += ministries[i]+', '*endTest
		self.hideMinistries()
		self.reviewText.SetLabel('Name: '+resultList[querySelection][1]+
			'\n'+servicesText+'\n'+ministriesText+'\nDate: '+
			datetime.datetime.now().strftime("%a %d %B, %Y")+'\nTime: '+
			datetime.datetime.now().strftime("%H:%M:%S"))
		self.showFinish()
		
		
	def cleanupQuery(self): #perform after a search to reset GUI
		global selectedServices
		global selectedMinistries
		self.listBox.Clear()
		self.search.SetValue('')
		for i in self.serviceButtons:
			i.SetValue(False)
		for i in self.ministryButtons:
			i.SetValue(False)
		selectedMinistries = []
		selectedServices = []
	
	def hideSearch(self):
		self.b1.Hide()
		self.b2.Hide()
		self.b3.Hide()
		self.b4.Hide()
		self.b5.Hide()
		self.b6.Hide()
		self.b7.Hide()
		self.b8.Hide()
		self.b9.Hide()
		self.b0.Hide()
		self.bAll.Hide()
		self.bClr.Hide()
		self.search.Hide()
		self.st1.Hide()
		self.statusText.Hide()
		self.searchb.Hide()
		self.register.Hide()
		self.exitb.Hide()
		self.stat.Hide()
		self.lastb.Hide()
		self.about.Hide()
		
	def showSearch(self):
		self.b1.Show()
		self.b2.Show()
		self.b3.Show()
		self.b4.Show()
		self.b5.Show()
		self.b6.Show()
		self.b7.Show()
		self.b8.Show()
		self.b9.Show()
		self.b0.Show()
		self.bAll.Show()
		self.bClr.Show()
		self.search.Show()
		self.st1.Show()
		self.statusText.Show()
		self.searchb.Show()
		self.register.Show()
		self.exitb.Show()
		self.stat.Show()
		self.lastb.Show()
		self.about.Show()
		self.search.SetFocus()
		
	def hideResult(self):
		self.listBox.Hide()
		self.st2.Hide()
		self.next1b.Hide()
		self.back1b.Hide()
		self.deleteb.Hide()
		self.statusText.SetLabel("""Ready: To begin, search by name, last four 
digits of phone number, or scan barcode.""")
		self.statusText.SetForegroundColour('dark green')
		
	def showResult(self):
		self.st2.SetLabel("Search Results. Please highlight your name and press 'Continue'")
		self.listBox.Show()
		self.st2.Show()
		self.next1b.Show()
		self.back1b.Show()
		self.deleteb.Show()
		
	def showServices(self):
		self.st2.SetLabel('Please select which services you will be serving')
		self.st2.Show()
		self.next2b.Show()
		self.back2b.Show()
		for i in self.serviceButtons:
			i.Show()
		self.serviceButtons[0].SetFocus()
		
	def hideServices(self):
		self.st2.Hide()
		self.next2b.Hide()
		self.back2b.Hide()
		for i in self.serviceButtons:
			i.Hide()
			
	def hideMinistries(self):
		self.st2.Hide()
		self.next3b.Hide()
		self.back3b.Hide()
		for i in self.ministryButtons:
			i.Hide()
			
	def showMinistries(self):
		self.st2.SetLabel('Where are you making a difference today?')
		self.st2.Show()
		self.next3b.Show()
		self.back3b.Show()
		for i in self.ministryButtons:
			i.Show()
		self.ministryButtons[0].SetFocus()
			
	def hideFinish(self):
		self.st2.Hide()
		self.reviewText.Hide()
		self.next4b.Hide()
		self.back4b.Hide()
		
	def showFinish(self):
		self.st2.SetLabel(
			'Please review the information below and press finish.')
		self.st2.Show()
		self.reviewText.Show()
		self.next4b.Show()
		self.back4b.Show()
		self.next4b.SetFocus()
		
	def hideRegister(self):
		self.registerFirst.Hide()
		self.registerLast.Hide()
		self.registerPhone.Hide()
		self.registerBarcode.Hide()
		self.registerBarcodeClear.Hide()
		self.registerAccept.Hide()
		self.registerCancel.Hide()
		self.registerSt1.Hide()
		self.registerSt2.Hide()
		self.registerSt3.Hide()
		self.registerSt4.Hide()
		
	def showRegister(self):
		self.registerFirst.Show()
		self.registerLast.Show()
		self.registerPhone.Show()
		self.registerBarcode.Show()
		self.registerBarcodeClear.Show()
		self.registerAccept.Show()
		self.registerCancel.Show()
		self.registerSt1.Show()
		self.registerSt2.Show()
		self.registerSt3.Show()
		self.registerSt4.Show()
		self.registerFirst.SetFocus()
		
	def registerCleanup(self, event):
		self.registerFirst.SetValue('')
		self.registerLast.SetValue('')
		self.registerPhone.SetValue('')
		self.registerBarcode.SetValue('')
		self.hideRegister()
		self.showSearch()
		
	def registerSave(self, event):
		first = self.registerFirst.GetValue()
		last = self.registerLast.GetValue()
		phone = self.registerPhone.GetValue()
		barcode = self.registerBarcode.GetValue()
		if '  ' in phone or len(phone) != 14:
			dial = wx.MessageDialog(None, 'Invalid phone number.',
				'Exclamation', wx.OK | wx.ICON_EXCLAMATION)
			dial.ShowModal()
			return 1
			
		#SQL to add a new row
		handler.Add(first, last, phone[1:4], phone[6:9], phone[10:14], 
			barcode)
		self.statusText.SetLabel(
			"%s was added successfully to the database" % first)
		self.notice("%s was added successfully to the database" % first)
		self.registerCleanup(event)
		
		
	def Register(self, event):
		self.hideSearch()
		self.showRegister()		
	
	def toggleService(self, Event, button):
		global selectedServices
		if selectedServices.count(button) == 0:
			selectedServices.append(button)
		else:
			selectedServices.remove(button)
		if len(selectedServices) == 0:
			self.next2b.Disable()
		else:
			self.next2b.Enable()
			
	def toggleMinistry(self, Event, button):
		global selectedServices
		if selectedMinistries.count(button) == 0:
			selectedMinistries.append(button)
		else:
			selectedMinistries.remove(button)
		if len(selectedMinistries) == 0:
			self.next3b.Disable()
		else:
			self.next3b.Enable()
			
	def submit(self, event):
		self.log()
		self.cleanupQuery()
		self.hideFinish()
		self.showSearch()
	
	def log(self):
		global resultList
		global querySelection
		global ministries
		global services
		global selectedServices
		global selectedMinistries
		global logFile
		selectedServices.sort()
		selectedMinistries.sort()
		servicesText = ''
		ministriesText = ''
		a = 0
		
		for i in selectedServices:
			a += 1  #counter
			#we use this to tell if we should add a comma to the list
			endTest = not(a == len(selectedServices))
			servicesText += services[i]+', '*endTest
			
		a = 0	
		for i in selectedMinistries:
			a += 1
			endTest = not(a == len(selectedMinistries))
			ministriesText += ministries[i]+', '*endTest
			
		f = open(logFile, 'rb')
		line = f.readline()
		f.close()
		if line[:4] != '"ID"':
			f = open(logFile, 'w')
			f.write('"ID","Name","Services served","Ministries served","Date","Time"\n')
			f.close()
		
		f = open(logFile, 'a')
		id = resultList[querySelection][0]
		name = resultList[querySelection][1]
		f.write(str(id)+',"'+name.replace('"','""')+'","'+
			servicesText+'","'+	ministriesText+'","'+
			datetime.datetime.now().strftime("%a %d %B, %Y")+'","'+
			datetime.datetime.now().strftime("%H:%M:%S")+'"\n')
		f.close()
		return 0
		
	def report(self, event):
		dial = wx.MessageDialog(self, 'Email report will be sent to info.journeychurch@gmail.com.',
				'Confirm', wx.OK | wx.CANCEL | wx.ICON_QUESTION)
		result = dial.ShowModal()
		dial.Destroy()
		if result == wx.ID_OK:
			global logFile
			result = mail.send('info.journeychurch@gmail.com', logFile)
			if result == 13:
				dial = wx.MessageDialog(None, 'Report file does not exist!',
					'Error', wx.OK | wx.ICON_ERROR)
				dial.ShowModal()
				dial.Destroy()
			if result == 0:
				#dial = wx.MessageDialog(None, 'Report sent.',
				#	'Information', wx.OK | wx.ICON_INFORMATION)
				#dial.ShowModal()
				#dial.Destroy()
				self.notice("Report was sent successfully.")
		self.showSearch()
		
	def notice(self, message):
		icon = "info"
		if "error" in message.lower():
			icon = "error"
		if "add" in message.lower():
			icon = "add"
		if "success" in message.lower():
			icon = "dialog-ok"
		n = pynotify.Notification("Taxidi", message, icon)
		n.show()		
	
	def OnQuit(self, event):
		global handler
		handler.Close()
		self.Destroy()
		
	def aboutTaxidi(self, event):
		info = wx.AboutDialogInfo()
		info.SetIcon(wx.Icon('resources/icon.png', wx.BITMAP_TYPE_PNG))
		info.SetName('Taxídí')
		info.SetVersion('0.10.0')
		info.SetDescription("""Taxídí is a volunteer tracking and nursery attendance database.
This version is a pre-alpha release inteded to track volunteers and create statistics for Journey Church of Millbrook, Alabama""")
		info.SetCopyright('© 2011 Zac Sturgeon')
		info.SetWebSite('http://www.jkltech.net/taxidi')
		info.SetLicence("""Taxidi is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free Software Foundation; 
either version 3 of the License, or (at your option) any later version.

Taxidi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have received a copy of 
the GNU General Public License along with File Hunter; if not, write to 
the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA""")
		info.AddDeveloper('Zac Sturgeon')
		info.AddDocWriter('Zac Sturgeon')
		wx.AboutBox(info)
		self.search.SetFocus()
		
		
		
application = wx.PySimpleApp()
# call class MyFrame
window = Main()
# start the event loop
application.MainLoop()

#exit after main loop
exit()
