#!/usr/bin/python

import matedb as db
import tempy
import safety
import images
import userlist
import privacy

def render(request):
    course = request['course'].value
    d = {'course': safety.make_safe(course)}
    d['members'] = userlist.format(db.get_course_members(course))
    
    return tempy.render('courses.template', d)
    
def get_courses_pane(user):
    if not privacy.permitted (user, 'courses'):
        return ''

    result = ''
    for course in db.get_all_courses(user):
        result += '<a href="?course=' + course + '"><p style="text-align: center">' + course + '</p></a>'
    return result
