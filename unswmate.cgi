#!/usr/bin/python
import cgi
from string import Template

import matedb
import head
import matelist
import images

# Enable errors-to-browser
import cgitb
cgitb.enable()

# Print the usual header
print "Content-Type: text/html"     
print                              


f = open('matepage.template', 'r');
template = Template(f.read())

form = cgi.FieldStorage()
if 'user' in form:
    user = form['user'].value
else:
    user = ''

if 'mood' in form and form['mood'].value == "sad":
    print '<iframe src="http://www.omfgdogs.com/" width="1920" height="1080" frameborder="0"></iframe>'

components = dict(
head = head.get_head(),
matelist = matelist.get_matelist(user)
)



data = dict(
user_username = matedb.get_data(user, 'username'),
user_profile_picture = images.get_profile_picture(user),
user_name = matedb.get_data(user, 'name'),
user_gender = matedb.get_data(user, 'gender'),
user_degree = matedb.get_data(user, 'degree'),
user_student_number = matedb.get_data(user, 'student_number'),
)

data.update(components)

print template.substitute(data)