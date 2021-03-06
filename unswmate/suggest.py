#!/usr/bin/python

import matedb as db
import authbar
import tempy
import images
import userlist

suggestions_per_page = 12

def do_suggest(request):
    user = authbar.get_current_login()
    
    if not user:
        return ''

    ranked_list = []
    for person, score in get_potential_mates(user).items():
        ranked_list.append((person, score,))
    
    if 'page' not in request:
        page = 0
    else:
        page = request['page'].value
        
    ranked_list.sort(key=lambda pair: pair[1])
    ranked_list.reverse()
    
    first = int(page) * suggestions_per_page
    last = first + suggestions_per_page

    data = dict(username = user, suggestions = '')

    renderlist = []
    for user in ranked_list[first:last]:
        renderlist.append(user[0]) 
    
    data['suggestions'] = userlist.render(renderlist)
        
    if data['suggestions']:
        data['next_page_link'] = '<a href="?action=suggest&page=' + (str(int(page) + 1)) + '">I need more!</a>'
    else:
        data['next_page_link'] = "There\'s no more... You need to go outside. Meet some new people. Make some real friends. Go. There's things the internet just can't offer."
        
    return tempy.render('suggest.template', data)
        
    
def get_potential_mates(user):
    # Yep, this is O(n^2). It also doesn't cache the result. Scaling
    # is something that happens to other people...

    scores = dict()
    current_mates = db.get_all_mates(user)
    for mate in current_mates:
        for person in db.get_all_mates(mate):
            if person not in current_mates and person != user:
                if person not in scores:
                    scores[person] = 0
                scores[person] += 1;

    for course in db.get_all_courses(user):
        for person in db.get_course_members(course):
            if person not in current_mates and person != user:
                if person not in scores:
                    scores[person] = 0
                scores[person] += 1;
    
    return scores
    
def get_suggest_pane(user):
    if authbar.get_current_login() != user: 
        return ''

    return '<div class="row-fluid"><div class="span12"><h3 style="text-align: center"><a href="?action=suggest">Find me some mates...</a></h3></div></div>'
        
def get_suggest_tab(user):
    if authbar.get_current_login() != user: 
        return ''
    else:
        return '<li><a href="#suggest" data-toggle="tab">Find Mates</a></li>'
