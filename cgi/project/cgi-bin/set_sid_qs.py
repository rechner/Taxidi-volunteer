#!/usr/bin/python
import cgi

def main():
	print "Content-type: text/html\n"
	try:
		import set_sid_qs_worker
	except:
		print "<!-- --><hr><h1>Oops.  An error occurred.</h1>"
	cgi.print_exception()

main()

