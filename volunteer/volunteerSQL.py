#!/usr/bin/env python
#-*- coding:utf-8 -*-

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

# Provides sqlite driver and database functions


import sqlite3

class Database:
	"""SQLite3 driver class for volunteer tracking database."""
	def __init__(self, file):
		"""Open connections to sqlite file; create if it doesn't exist"""
		try:
			fh = open(file)
			fh.close()
		except IOError as e:
			print("({0})".format(e))
			print "Warning: database file does not exist; creating "+file
			#file does not exist, so create the table.
			self.conn = sqlite3.connect(file)
			self.cursor = self.conn.cursor()
			self.CreateTables()
			self.conn.commit()
			self.conn.close()
		#open database for writing/query
		self.conn = sqlite3.connect(file)
		self.cursor = self.conn.cursor()
		
	def Add(self,Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode):
		"""Add row into database"""
		try:
			self.cursor.execute('INSERT INTO data(Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode) VALUES (?,?,?,?,?,?)',
			(Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode))
		except:
			#create tables if they don't exist yet.
			self.CreateTables()
			self.cursor.execute('INSERT INTO data(Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode) VALUES (?,?,?,?,?,?)',
			(Name,lName,PhoneArea,PhonePre,PhonePrimary,Barcode))
		self.conn.commit()
		print "Debug: committed database successfully"
		
	def CreateTables(self):
		try:
			self.cursor.execute("""CREATE TABLE data(id integer primary key, Name text, 
			lName text, PhoneArea integer, PhonePre integer, PhonePrimary integer, Barcode text)""")
			self.cursor.execute("CREATE TABLE services(id integer primary key, Description text)")
			self.cursor.execute("CREATE TABLE ministries(id integer primary key, Description text, Note)")
			self.cursor.execute("""CREATE TABLE statistics(id integer primary key, record integer, Name text, lName text, 
			ministries text, services text, date text, time text)""")
		except:
			print "TaxidiDB: Some tables already created, skipping..."
			
	def ReturnAll(self):
		"""Return every row from the database"""
		rows = self.cursor.execute('SELECT * FROM data').fetchall()
		return rows
		
	def Query(self, query):
		"""Query the database with either last name, last 4 digits of phone #, or barcode."""
		rows = self.cursor.execute("SELECT * FROM data WHERE phonePrimary=? OR Barcode=? OR lName LIKE ?", (query, query, query)).fetchall()
		return rows
		
	def Delete(self, index):
		ret = self.cursor.execute("DELETE FROM data WHERE id=?", (index,))
		self.conn.commit()
		return ret
		
	def Close(self):
		a = self.cursor.close()
		return a
		


# Tables:
# Services: (id, description)
# e.x.  ( '0', 'First Service' ; '1', 'Second Service')

# Ministires: (id, description)
# e.x. ( '0', 'Parking'


#handler = Taxidi(fileName)
#handler.Add('Sally', 'Smith', '703', '555', '2345', 'ABC 123')
#print handler.ReturnEntries()
#print handler.Query('ABC 123')
#exit()
