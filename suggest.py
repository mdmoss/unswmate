#!/usr/bin/python

import matedb

def get_potential_mates(user):
    scores = {}
    current_mates = matedb.get_all_mates(user)
    for mate in current_mates:
        for person in matedb.get_all_mates(mate):
            if person not in current_mates:
                if person not in scores:
                    scores[person] = 0
                scores[person] += 1;

    for course in matedb.get_all_courses(user):
        for person in matedb.get_course_members(course):
            if person not in current_mates:
                if person not in scores:
                    scores[person] = 0
                scores[person] += 1;
    
    return scores
