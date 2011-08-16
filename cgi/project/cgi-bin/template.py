#!/usr/bin/env python
#-*- coding:utf-8 -*-

def head(title, user):
	if len(title) == 0:
		title = "Taxidi | Search gateway"
		
	if len(user) == 0:
		userhtml = """<div style="position: absolute; top: 10; right: 10; width: 300px; text-align:right; font-family:verdana; color:#ffffff; font-size=3"> 
Welcome, ~<b><a href="cgi-bin/usercp.cgi" style="color:#ffffff" >"""+user+"""</a></b><br> 
<a href="cgi-bin/logout.cgi" style="color:#ffffff; font-size:80%">logout</a> 
</div> """

	return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>"""+title+"""</title>
<meta http-equiv="Content-Type" content=
  "text/html; charset=utf-8">
</head>
<body style="background-repeat:repeat-x; background-color:#ededed" background="/pixmaps/background.png">
<link rel="icon" type="image/png" href="/pixmaps/Taxidi.png">
<img style="position:absolute; top:0px; left:-1px" src="/pixmaps/header.png" width="781" height="240" />
<a href="#"><img style="position:absolute; top:137px; left:70px" src="/pixmaps/home2.png" border="0" /></a>

""" + userhtml +"""

<DIV style="position: absolute; top:220px; left:50px; width:780px"><h3 style="font-family:verdana"></h3> <p style="font-family:verdana; font-size:80%">"""


def foot():
	return "</div></body></html>"
	
def login(message):
	return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
<meta http-equiv="Content-type" content="text/html;charset=UTF-8" >
<title>Taxidi | Search gateway login</title>
</head>

<body style="background-repeat:repeat-x; background-color:#ededed" background="/pixmaps/background.png">
<img style="position:absolute; top:0px; left:-1px" src="/pixmaps/header.png" width="361" height="240" alt="logo">

<a href="#"><img style="position:absolute; top:137px; left:70px" src="/pixmaps/login2.png" border="0" alt="logo"></a>

<DIV style="position: absolute; top:220px; left:50px">


<table border = 0 style="font-family:verdana">
<tr><td align="center" width="60%">
<h3 style="font-family:verdana; color:red">System Login - WARNING</h3>
<p style="font-family:verdana; color:red"><u>THIS IS A PRIVATE COMPUTER SYSTEM</u></p>
<p style="font-family:verdana; font-size:12px">This computer system including all related equipment, network devices (specifically including Internet access), are provided only for authorized use. All computer systems may be monitored for all lawful purposes, including to ensure that their use is authorized, for management of the system, to facilitate protection against unauthorized access, and to verify security procedures, survivability and operational security. Monitoring includes active attacks by authorized personnel and their entities to test or verify the security of the system. During monitoring, information may be examined, recorded, copied and used for authorized purposes. All information including personal information, placed on or sent over this system may be monitored. Uses of this system, authorized or unauthorized, constitutes consent to monitoring of this system. Unauthorized use may subject you to criminal prosecution. Evidence of any such unauthorized use collected during monitoring may be used for administrative, criminal or
other adverse action. Use of this system constitutes consent to monitoring for these purposes.<br>
<br>
By accessing this system, you consent to the above statement.</p>
</td>
<td align="center" width="40%">
<table border = 0 style="font-family:verdana; font-size:16px" cellpadding=16>
<tr><td align="center"><b>Dreamteam Login</b></td></tr></table>

<table border=0 style="font-family:verdana; font-size:13px; color:red">
<tr><td align="center">"""+message+"""</td></tr>
</table>

<FORM METHOD = post ACTION = "/cgi-bin/auth.cgi">
<TABLE BORDER = 0 style="font-family:verdana; font-size:80%">
<TR><TD align="right">Username:</TD>
<TD><INPUT type = text name = "user"></TD></TR>
<TR><TD align="right">Password:</TD>
<TD><INPUT type = password name = "pass"></TD>
<TR><TD></TD><TD><CENTER><INPUT TYPE = submit VALUE = "Login"></CENTER>
<INPUT TYPE = hidden NAME = "action" VALUE = "display"></TD></TR>

</TABLE>
</FORM>
</td></tr></table>



<script language="JavaScript" type="text/javascript">
<!--
function set_focus()
{
    document.forms[0].user.focus();
}

set_focus();
//-->
</script>

<br><br><br><br>
<center><div style="font-family:verdana; font-size:10px; color:#aaaaaa">Taxídí and the Taxídí logo are © 2011 JKL Tech, Inc.  All rights reserved.  Written for Journey Church in Millbrook, Alabama</div></center>

</div>
</body>
</html>
"""


