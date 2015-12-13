import yaml, json, sys, os

COURSES_DIR = 'data/courses'


def make_courses_list(courses_list, courses_data):
    ret = []
    for sid, study in enumerate(courses_list['studies']):
        for period in study['periods']:
            for cid, course in enumerate(period['courses']):
                o = courses_data.get(course['id'], {})
                o['id'] = course['id']
                if 'grade' in course:
                    o['grade'] = course['grade']
                o['universityStudiesId'] = sid + 1
                o['academicYear'] = period['year']
                if 'literature' not in o: o['literature'] = '-'
                ret.append(o)

    return ret

def display_status(courses):
    def cut(s, n): return ("{:"+str(n)+"}").format(s)[:n]

    print("id             words           Wk Le Tu Pr Re ECTS  title")
    for c in l:
        line = cut(c['id'], 15)
        hasContent = 'content' in c
        if not hasContent:
            print(line)
            continue

        n = len(c['content'])
        contentLengthOk = n <= 500
        hasWeeksAndCredits = 'weeks' in c and 'credits' in c
        hashours = 'hoursLectures' in c or 'hoursPracticalWork' in c

        line += cut(str(n), 6)
        line += "x" if contentLengthOk else " "
        line += " "
        line += "x" if hasWeeksAndCredits else " "
        line += " "
        line += "x" if hashours else " "

        line += "     "
        fields = ['weeks', 'hoursLectures', 'hoursTutorial', 'hoursPracticalWork', 'hoursResearch', 'credits']
        for f in fields:
            line += "%2d " % c[f] if f in c else "   "

        line += "   " + c.get('title', '')

        print(line)



with open("mycourses.yml") as f:
    courses_list = yaml.load(f)

courses_data = {}
for dirname, dirnames, filenames in os.walk(COURSES_DIR):
    for filename in filenames:
        with open(os.path.join(dirname, filename)) as f:
            o = yaml.load(f)
            if o is not None:
                courses_data.update(o)

l = make_courses_list(courses_list, courses_data)
display_status(l)

with open("merged.yml", "w") as f:
    yaml.safe_dump({'courses':l}, f)
