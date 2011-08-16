#! /usr/bin/python
#-*- coding:utf-8 -*-

import cgi
import os, sys
import commands

print "Content-Type: text/html; charset=\"utf-8\"\n\n"

form = cgi.FieldStorage()

if (form.has_key("action") and form.has_key("search")):
	if (form["action"].value == "display"):
		query = form['search'].value  # Input from text box (read into the string 'query'
		opt = form.getvalue('opt')
		if query == "": 					# skip search if input is blank.
			exit()
		if str(opt) == 'None':
			opt = ""
		print "<html><body><center>"
		print "<h1><i>Ergebnisse für </i>„"+query+"“</h1>"

		pre = commands.getoutput("/bin/egrep -h "+opt+" -i -e '"+query+"' /usr/share/trans/de-en")

		if pre.strip() == '':
			print "<b>Kein Ergebnis</b>"
			print """<br><br><br><TABLE BORDER = 0><FORM METHOD = post ACTION = \"ding.cgi\">
			<TR><TH>wieder suchen:</TH><TD><INPUT type = text name = \"search\"><INPUT TYPE = submit VALUE = \"Suche\"></TD>
			</TABLE>
			<INPUT TYPE = hidden NAME = \"action\" VALUE = \"display\">
			</FORM></center></body></html>"""
			exit()
			
		
		#print "<pre>"+pre+"</pre><br><br><br>"
		
		print "<center><i>(Ergebnissen: "+str(len(pre.split('\n')))+")</i><br><br>"
		print "<table border=\"1\"><th>Deutsch</th><th>English</th>"

		pre2 = pre.split('\n')
		pre2 = pre.replace(query.strip(), "<font style=\"BACKGROUND-COLOR: yellow\">"+query+"</font>").split('\n') #highlight the search
		#pre3 = pre2.replace(' | ', '<br>')
		
			
		for i in pre2:
			print "<tr><td><b>"+i.replace(' | ', '<br>').split('::')[0]+"</b></td><td> "+i.replace(' | ', '<br>').split('::')[1]+"</td></tr>"
		
		print "</table>"
		print """<br><br><br></center><center><TABLE BORDER = 0><FORM METHOD = post ACTION = \"ding.cgi\">
			<TR><TH>wieder suchen:</TH><TD><INPUT type = text name = \"search\"><INPUT TYPE = submit VALUE = \"Suche\"></TD>
			</TABLE>
			<table border = 0>
			<tr><td><input type="radio" name="opt" value=""> Teilsuche</td>
			<td><input type="radio" name="opt" value="-w" checked> Ganz Wörter</td></table>
			<INPUT TYPE = hidden NAME = \"action\" VALUE = \"display\">
			</FORM></center></body></html>"""
		
		
else:
	print """
	<html>
	<head>
	<title>Das Ding -- Suchen</title>
	</head>
	<body>
	
	<center>
	<h1>Das Ding Wörterbuch</h1>
	<TABLE BORDER = 0>
	<FORM METHOD = post ACTION = \"ding.cgi\">
	<TR><TH>Suchwort:</TH><TD><INPUT type = text name = \"search\"><INPUT TYPE = submit VALUE = \"Suche\"></TD>
	</TABLE>
	<table border = 0>
	<tr><td><input type="radio" name="opt" value=""> Teilsuche</td>
	<td><input type="radio" name="opt" value="-w" checked> Ganz Wörter</td></table>
	<INPUT TYPE = hidden NAME = \"action\" VALUE = \"display\">
	</FORM>
	</center>

	</body>
	</html>"""

