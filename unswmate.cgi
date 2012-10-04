#!/usr/bin/python
import cgi

# Enable errors-to-browser
import cgitb
cgitb.enable()

# Print the usual header
print "Content-Type: text/html"     
print                              

# This is lazy
print '<link href="css/bootstrap.min.css" rel="stylesheet">'

f = open('sidebar.template', 'r');
print f.read()
