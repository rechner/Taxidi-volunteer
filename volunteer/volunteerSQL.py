#!/usr/bin/env python

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


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
		try:
			self.cursor.execute("""CREATE TABLE data(id integer primary key, Name text, 
			lName text, PhoneArea integer, PhonePre integer, PhonePrimary integer, Barcode text)""")
			self.cursor.execute("CREATE TABLE services(id integer primary key, Description text)")
			self.cursor.execute("CREATE TABLE ministries(id integer primary key, Description text, Note)")
			self.cursor.execute("""CREATE TABLE statistics(id integer primary key, record integer, Name text, lName text, 
			ministries text, services text, date text, time text)""")
		except:
			print "TaxidiDB: Some tables already created, skipping..."
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
