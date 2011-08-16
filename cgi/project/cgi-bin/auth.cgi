#!/usr/bin/env python
#-*- coding:utf-8 -*-

#Login.  Uses independent crypt database.

# Psuedocode:
# Check if browser has cookie, get cookie value
# if cookie is expired, then remove the session and redirect to login
# if cookie is valid, find matching session.  If session is still valid redirect to home
# else:
# login
# test(id, passwd)
# if valid, then grant cookie and redirect to home.

#DEBUG:
import cgitb; cgitb.enable()

import os, sys
import hashlib
import cgi
import session, time
import template

sys.path.append(os.environ['DOCUMENT_ROOT'])

global shadow, salt

salt = "h193dc%"
shadow = "shadow"  #shadow file

form = cgi.FieldStorage() # instantiate only 

# test a password
def test(id, passwd):
	pre = []
	user = []
	hash = []
	
	f = open(shadow, 'r')
	
	for i in f:
		if i != "\n":
			pre.append(i[:(len(i)-1)]) #remove the end \n
			
	for i in pre:
		user.append(i.split(':')[0])
		hash.append(i.split(':')[1])
	
	#test for user
	pos = [i for i,x in enumerate(user) if x == id] #returns positon of user in list
	if len(pos) == 0:
		return "baduser"
	if hashlib.sha1(passwd+salt).hexdigest() == hash[pos[0]]:
		return "success"
	else:
		return "fail"
		
def granted():
	# Access granted.  Make cookies, etc. yay
	#import index.cgi
	print "Granted! Cue redirect..."
	sess.data['lastvisit'] = repr(time.time())
	sess.data['user'] = user


sess = session.Session(expires=1*24*60*60, cookie_path='/')
#session data is a dictionary-like object

lastvisit = sess.data.get('lastvisit')
authuser = sess.data.get('user')	#see if they have a valid cookie

user = form.getfirst('user', 'empty')
passwd = form.getfirst('pass', 'empty')

user = cgi.escape(user)			#sanitize the input (no injections >:3)
passwd = cgi.escape(passwd)

print "Content-Type: text/html\n\n"

if authuser != 'noauth':
	print granted()
	exit()

if user == 'empty' or not authuser:
	#placeholder cookie; so we know they generated the page...
	sess.data['user'] = 'noauth'
	print template.login('')
	exit()

challenge = test(user, passwd)
if challenge == "baduser" or challenge == "fail":
	print template.login('<b>Bad username or password</b>')
	
	
if challenge == "success":
	granted()
	
	
