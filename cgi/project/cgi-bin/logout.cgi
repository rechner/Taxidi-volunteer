#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.environ['DOCUMENT_ROOT'])

import session, time
import template

#expire the cookie, deauthorize the session key
sess = session.Session(expires=1*24*60*60, cookie_path='/')
sess.set_expires('')
sess.data['user'] = 'noauth'
sess.data['lastvisit'] = repr(time.time())

print "Content-Type: text/html\n\n"
print template.login('Successfully logged out')
