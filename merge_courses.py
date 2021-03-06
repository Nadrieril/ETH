#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml, json, sys, os
from termcolor import colored
import colorama; colorama.init() # Cross-platform colors

COURSES_DIR = 'data/courses'

def load_course_data():
    courses_data = {}
    for dirname, dirnames, filenames in os.walk(COURSES_DIR):
        for filename in filenames:
            with open(os.path.join(dirname, filename)) as f:
                o = yaml.load(f)
                if o is not None:
                    courses_data.update(o)

    return courses_data

def make_courses_list(courses_list, courses_data):
    ret = []
    for sid, study in enumerate(courses_list['studies']):
        for period in study['periods']:
            l = [(2, c) for c in period.get('projects', [])] + [(1, c) for c in period.get('courses', [])]
            for cat, course in l:
                o = {}
                if course['id'] in courses_data:
                    o.update(courses_data[course['id']])
                o.update(course)
                o['completed'] = study['completed']
                o['universityStudiesId'] = sid + 1
                o['subjectCategory'] = cat
                o['academicYear'] = period['year']
                if 'literature' not in o: o['literature'] = '-'
                ret.append(o)

    return ret

def validate(c):
    errors = []
    def err(s): errors.append({'id': c['id'], 'msg': s, 'err': True})
    def warn(s): errors.append({'id': c['id'], 'msg': s, 'err': False})

    hasContent = 'content' in c
    if not hasContent:
        err("Le cours n'a pas de description")
    else:
        n = len(c['content'])
        if n > 500:
            err("La description fait plus de 500 caractères (%d)" % n)

    hasHours = c['subjectCategory']==1 and ('hoursLectures' in c or 'hoursPracticalWork' in c or 'hoursTutorial' in c) \
                or c['subjectCategory']==2 and 'hoursResearch' in c
    if not hasHours:
        err("Le nombre d'heures par semaine n'est pas indiqué")

    hasWeeks = 'weeks' in c
    if not hasWeeks:
        err("Le nombre de semaines n'est pas indiqué")

    hasCredits = 'credits' in c
    if c['completed'] and not hasCredits:
        warn("Le nombre de crédits n'est pas indiqué")

    hasGrade = 'grade' in c
    if c['completed'] and not hasGrade:
        warn("La note n'est pas indiquée")

    return errors

def compute_errors(courses):
    def flatten(l): return [x for xs in l for x in xs]
    return flatten(validate(c) for c in courses)

def display_status(courses):
    def cut(s, n): return ("{:"+str(n)+"}").format(s)[:n]
    def cutr(s, n): return ((" "*n)+s)[-n:]

    print("id                  words  weeks lect tuto prac  res ECTS grade    title")
    for c in l:
        line = cut(c['id'], 20)
        hasContent = 'content' in c
        if not hasContent:
            print(line)
            continue

        n = len(c['content'])
        contentLengthOk = n <= 500

        line += colored("%5d" % n, 'green' if contentLengthOk else 'red')
        line += " "

        line += "%6d" % c['weeks'] if 'weeks' in c else colored('    ??', 'red')
        line += " "

        hasHours = c['subjectCategory'] == 1 and ('hoursLectures' in c or 'hoursPracticalWork' in c or 'hoursTutorial' in c) \
                    or c['subjectCategory'] == 2 and 'hoursResearch' in c
        hasHours = 'hoursLectures' in c or 'hoursPracticalWork' in c or 'hoursTutorial' in c or 'hoursResearch' in c
        if hasHours:
            fields = ['hoursLectures', 'hoursTutorial', 'hoursPracticalWork', 'hoursResearch']
            for f in fields:
                line += cut("%4d" % c[f] if f in c else "", 4)
                line += " "
        else:
            if c['subjectCategory'] == 1:
                line += colored("  ??   ??   ??      ", 'red')
            else:
                line += colored("                 ?? ", 'red')

        line += "%4d" % c['credits'] if 'credits' in c else "    "
        line += " "

        line += cutr(c['grade'] if 'grade' in c else "", 5)
        line += " "


        line += "   "
        line += c.get('title', '')

        print(line)


with open("mycourses.yml") as f:
    courses_list = yaml.load(f)

courses_data = load_course_data()

l = make_courses_list(courses_list, courses_data)
display_status(l)

for x in compute_errors(l):
    err = "Err " if x['err'] else "Warn"
    print("[%s] %s: %s" % (err, x['id'], x['msg']))

for x in l:
    del x['id']
    del x['completed']

with open("merged.yml", "w") as f:
    yaml.safe_dump({'courses':l}, f, default_flow_style=False)
