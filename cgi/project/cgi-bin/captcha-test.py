#!/usr/bin/env python
#-*- coding:utf-8 -*-

import template as html

DEBUG_TO_WEB = True
RECAPTCHA_PUBLIC_KEY = '6Lcw2sMSAAAAAI5YBur4sDO-fxoZHYAwj50_FOGC'
RECAPTCHA_PRIVATE_KEY = '6Lcw2sMSAAAAAOhBVS171XQiSZq0n86uB8HQM1UU'

FORM_PAGE_TEMPLATE="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <title>Registration</title>
  <meta http-equiv="Content-Type" content=
  "text/html; charset=utf-8">
</head>
<body>
  <form class="feedback-form" name="feedback_form" id="feedback_form" method="post"
        action="%(scriptname)s">
    <div class="captcha">
      %(captcha)s
    </div>
     <p><input type="submit" value="Submit"></p>
  </form>
</body>
</html>"""

RESPONSE_PAGE_TEMPLATE="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <title>%(title)s</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <link rel="stylesheet" href="stylee.css" type="text/css" />
</head>
<body>
  <h2>%(title)s</h2>
  %(response)s
</body>
</html>"""


def webit():
	import os,cgi
	from exceptions import Exception
	from recaptcha.client import captcha
	
	try:
		scriptname=os.environ['SCRIPT_NAME']
	except: 
		raise Exception,'Program should run as a cgi'
	if DEBUG_TO_WEB:
		import cgitb; cgitb.enable()
	
	print 'Content-type: text/html; charset=utf-8\n\n'
	form = cgi.FieldStorage()
	if os.environ['REQUEST_METHOD']=='GET':
		print FORM_PAGE_TEMPLATE % {
			'scriptname':scriptname,
			'errorhtml':'',
			'captcha':captcha.displayhtml(RECAPTCHA_PUBLIC_KEY),
		}
		
	
	
	else: # POST
		errors=[]
		captcha_error=''

		captcha_response = captcha.submit(
			form.getvalue('recaptcha_challenge_field'),
			form.getvalue('recaptcha_response_field'),
			RECAPTCHA_PRIVATE_KEY,
			os.environ['REMOTE_ADDR'])	
		if not captcha_response.is_valid:
			errors.append("You've failed the captcha test. Convince me again that you're not a robot.")
			captcha_error=captcha_response.error_code
		if errors:
			errorhtml='<ul class="error-list">%s</ul>' % ('\n'.join(['<li>%s</li>' % e for e in errors]))
			print FORM_PAGE_TEMPLATE % {
				'scriptname':scriptname,
				'errorhtml':errorhtml,
				'captcha':captcha.displayhtml(RECAPTCHA_PUBLIC_KEY,error=captcha_error),
			}
		else:
			try:
				title = 'Action completed'
				response = 'Thank you.  The form has been submitted to a moderator for review.'
			except Exception,e:
				title = 'Failed'
				response = '<strong>Error:</strong> %s' % str(e)
			print RESPONSE_PAGE_TEMPLATE % {'title':title,'response':response}
	
		
if __name__=='__main__':
	webit()
