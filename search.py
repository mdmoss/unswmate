#!/usr/bin/python

import matedb
import tempy
import images
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

    template = Template(open('search_result.template', 'r').read())
    full_string = "";

    for result in results:
        data = dict(
            profile_picture = images.get_profile_picture(result),
            user_page = cgienv.get_URL() + "?who=" + result
        )
        data.update(matedb.get_user_data (result))
        full_string += template.safe_substitute(data) 

    return full_string

def search(term):
    results = matedb.search_like(term, 'username')
    results += matedb.search_like(term, 'name')
    return set(results)
