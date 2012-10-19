#!/usr/bin/python
import cgi

import config

import authbar
import editor
import create
import upload
import mate
import search
import suggest
import matepage
import tempy
import courses
import privacy
import news
import homepage

def serve():
    if config.debug:
        # Enable errors-to-browser
        import cgitb
        cgitb.enable()

    # Print a common header
    print "Content-Type: text/html"
    print

    # You may be wondering how we're going to handle cookies, because normally
    # they're placed in the header. There's going to be some javascript magic!
    c = cgi.FieldStorage()      

    if config.debug:
        for key in c.keys():
            print key + " => " + c[key].value
      
    def handle_error(request):
        return "An error occured, and was caught. Whoops..."
          
    # Actions have priority in our routing system
    if 'action' in c:

        actions = {
            'login': authbar.do_login,
            'logout': authbar.do_logout,
            'edit': editor.do_edit,
            'create': create.do_create,
            'upload': upload.do_upload,
            'mate': mate.do_mate,
            'suggest': suggest.do_suggest,
            'privacy': privacy.do_privacy,
            'news': news.do_news,
            'comment': news.do_comment,
        }
        
        chosen = c['action'].value
        result = actions.get(chosen, handle_error)(c)

    # Are they looking for course info?        
    elif 'course' in c:
        result = courses.render(c)  
         
    # Was it a search?
    elif 'search' in c:
       result = search.render(c)  

    # Or at least an ordinary matepage
    elif 'who' in c:
        result = matepage.render()

    # At worst, show the home screen 
    else:      
        result = homepage.render()

    print tempy.insert_head(result); 
        
