#!/usr/bin/python
import cgi
from string import Template

import matedb
import head
import matelist
import matepage
import authbar
import cgienv
import search
import editor

# Enable errors-to-browser
import cgitb
cgitb.enable()

# Print a common header
print "Content-Type: text/html"
print

# You may be wondering how we're going to handle cookies, because normally
# they're placed in the header. There's going to be some javascript magic!
c = cgi.FieldStorage()      

# Debug!
for key in c.keys():
    print key + " => " + c[key].value
  
def handle_error():
    print "An error occured, and was caught. Whoops..."
      
# Actions have priority in our routing system

if 'action' in c:

    actions = {
        'login': authbar.do_login,
        'logout': authbar.do_logout,
        'edit': editor.do_edit,
    }
    
    chosen = c['action'].value
    actions.get(chosen, handle_error)(c)

# Followed by pages
      
elif 'page' in c:

    pages = dict(
    )
    
    chosen = c['page'].value
    print pages[chosen]()
     
# Was it a search?

elif 'search' in c:

   print search.render(c)  

# Or at least an ordinary matepage

elif 'who' in c:
    print matepage.render()

# At worst, show a welcome screen
      
else:      
    print matepage.render()
    
