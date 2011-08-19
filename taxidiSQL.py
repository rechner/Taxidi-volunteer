#!/usr/bin/env python
import sqlite3

fileName = 'users.db' # what database file to use

class Taxidi:
	def __init__(self,file):
		try:
			fh = open(file)
			fh.close()
		except IOError as e:
			#print("({})".format(e))
			print "Warning: database file does not exist; creating "+file
			#file does not exist, so create the table.
			self.conn = sqlite3.connect(file)
			self.cursor = self.conn.cursor()
			self.createTables()
			self.conn.commit()
			self.conn.close()
		#open database for writing/query
		self.conn = sqlite3.connect(file)
		self.cursor = self.conn.cursor()
	def addEntry(self,Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode):
		try:
			self.cursor.execute('INSERT INTO data(Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode) VALUES (?,?,?,?,?,?)',
			(Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode))
		except:
			self.createTables()
			self.cursor.execute('INSERT INTO data(Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode) VALUES (?,?,?,?,?,?)',
			(Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode))
		self.conn.commit()
	def createTables(self):
		self.cursor.execute("""CREATE TABLE data(id integer primary key, Name text, 
		lName text, PhoneArea integer, PhonePre integer, PhonePrimary integer, Barcode text)""")
	def returnEntries(self):
		rows = self.cursor.execute('SELECT * FROM data').fetchall()
		return rows
		


# Tables:
# Services: (id, description)
# e.x.  ( '0', 'First Service' ; '1', 'Second Service')

# Ministires: (id, description)
# e.x. ( '0', 'Parking'


handler = Taxidi(fileName)
handler.addEntry('John', 'Smith', '703', '555', '5555', 'ABC123')
print handler.returnEntries()
exit()
