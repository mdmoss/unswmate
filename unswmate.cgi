#!/usr/bin/python
import cgi
from string import Template

import matedb
import head

# Enable errors-to-browser
import cgitb
cgitb.enable()

# Print the usual header
print "Content-Type: text/html"     
print                              


f = open('matepage.template', 'r');
template = Template(f.read())

components = dict(
head = head.get_head()
)

form = cgi.FieldStorage()
user = form['user'].value

data = dict(
user_username = matedb.get_data(user, 'username'),
user_name = matedb.get_data(user, 'name'),
user_email = matedb.get_data(user, 'email'),
user_gender = matedb.get_data(user, 'gender'),
user_degree = matedb.get_data(user, 'degree'),
user_student_number = matedb.get_data(user, 'student_number'),
)

data.update(components)

print template.substitute(data)