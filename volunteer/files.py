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

# Provides basic file operations (copying was needed)

def copy(source, dest, buffer_size=1024*1024):
	"""
	Copy a file from source to dest. source and dest
	can either be strings or any object with a read or
	write method, like StringIO for example.
	"""
	if not hasattr(source, 'read'):
		source = open(source, 'rb')
	if not hasattr(dest, 'write'):
		dest = open(dest, 'wb')
		
	while 1:
		copy_buffer = source.read(buffer_size)
		if copy_buffer:
			dest.write(copy_buffer)
		else:
			break

	source.close()
	dest.close()
