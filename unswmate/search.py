#!/usr/bin/python

import matedb as db
import tempy
import images as images
import cgienv
from string import Template
from safety import make_safe

def render(request):
    searchterm = request['search'].value
    results = search(searchterm)
    if results:
        result_string = render_results(results)
    else:
        result_string = "No Results for " + make_safe(searchterm)

    data = dict(
        search_result = result_string
    )
    
    return tempy.render('search.template', data)


def render_results(results):

    full_string = "";

    for result in results:
        data = dict(
            profile_picture = images.get_profile_picture(result),
            user_page = cgienv.get_URL() + "?who=" + result
        )
        data.update(db.get_user_data (result))
        full_string += tempy.substitute('search_result.template', data)

    return full_string

def search(term):
    results = db.search_like(term, 'username')
    results += db.search_like(term, 'name')
    return set(results)
