#!/usr/bin/python

import sha, time, Cookie, os, shelve

class Session(object):

	def __init__(self, expires, cookie_path):
		string_cookie = os.environ.get('HTTP_COOKIE', '')
		self.cookie = Cookie.SimpleCookie()
		self.cookie.load(string_cookie)
		
		if self.cookie.get('sid'):
			sid = self.cookie['sid'].value
			# clear SID from other cookies
			self.cookie.clear()
			
		else:
			self.cookie.clear()
			sid = sha.new(repr(time.time())).hexdigest()
			
		self.cookie['sid'] = sid
		
		if cookie_path:
			self.cookie['sid']['path'] = cookie_path
			
		#session_dir = os.environ['DOCUMENT_ROOT'] + '/session'
		session_dir = '/tmp/session'
		
		if not os.path.exists(session_dir):
			try:
				os.mkdir(session_dir, 02770)
			except OSError, e:
				errmsg = """%s when trying to create session directory. \
create it as '%s'""" % (e.strerror, os.path.abspath(session_dir))
				raise OSError, errmsg
		self.data = shelve.open(session_dir + '/sess_' + sid, writeback=True)
		os.chmod(session_dir + '/sess_' + sid, 0660)
		
		#init the expires data
		if not self.data.get('cookie'):
			self.data['cookie'] = {'expires':''}
			
		self.set_expires(expires)
		
	def close(self):
		self.data.close()
		
	def set_expires(self, expires):
		if expires == '':
			self.data['cookie']['expires'] = ''
		elif isinstance(expires, int):
			self.data['cookie']['expires'] = expires
		
		self.cookie['sid']['expires'] = self.data['cookie']['expires']
		
