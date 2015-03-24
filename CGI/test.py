#!/usr/bin/python
# coding: utf-8

import cgi
import os
# import cgitb
# cgitb.enable()

print 'Content-Type: text/html\n\n'
print "Hello world!"


# GETメソッドであるか調べる
if os.getenv('REQUEST_METHOD') == "POST" :
	form = cgi.FieldStorage()
	print "POST::"
	print form.getvalue('code', 'none')
	print form.getvalue('lang', 'none')

	if form.haskey("code"):
		print "haskey"
	else:
		print "nokey"
	print "aa"
	print form["code"].value

