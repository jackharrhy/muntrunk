from urllib.parse import urlparse, parse_qs
import shelve
import re
import requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www5.mun.ca",
    "Connection": "keep-alive",
    "Referer": "https://www5.mun.ca/admit/hwswsltb.P_CourseSearch?p_term=201902&p_levl=01*04",
    "Upgrade-Insecure-Requests": "1",
}

data = {
    "p_term": "201902",
    "p_levl": "01*04",
    "campus": "St. John's",
    "faculty": "%",
    "prof": "%",
    "crn": "%",
}


def fresh_entire_resp():
    return requests.post(
        "https://www5.mun.ca/admit/hwswsltb.P_CourseResults", headers=headers, data=data
    )


def grab_entire_resp():
    with shelve.open("persist") as db:
        if not "entire_resp" in db:
            entire_resp = fresh_entire_resp()
            db["entire_resp"] = entire_resp
            return entire_resp
        else:
            return db["entire_resp"]


def default_parser(field):
    field = field.strip()

    if field == "":
        return None

    try:
        return int(field)
    except ValueError:
        return field


def bool_parser(field):
    field = field.strip()
    fields = field.split(" ")
    if len(fields) == 1:
        return bool(fields[0])
    elif len(fields) == 2:
        return [bool(fields[0]), bool(fields[1])]
    else:
        raise "found a boolean field with > 2 fields!"


def ignore_parser(field):
    return None


def days_of_the_week_parser(field):
    fields = field.strip().split(" ")
    fields = [x for x in fields if x]
    return fields


def course_name_parser(field):
    return {"subject": field[:4], "number": field[5:9], "name": field[10:].strip()}


# TODO parse multiple instructors per course
def instructor_parser(field):
    parts = field.split(" - ")
    if len(parts) != 2:
        return None
    else:
        return {"type": parts[0], "name": parts[1]}


class FieldParser:
    def __init__(self, name, parse_function=default_parser):
        self.name = name
        self.parse = parse_function


class CourseParser:
    course_name_regex = re.compile("([A-Z]){4} \d{4}")

    index_map = {
        0: FieldParser("course", course_name_parser),
        1: FieldParser("section"),
        2: FieldParser("crn"),
        3: FieldParser("slot"),
        4: FieldParser("days", days_of_the_week_parser),
        5: FieldParser("begin"),
        6: FieldParser("end"),
        7: FieldParser("room"), # TODO parse one char room names
        8: FieldParser("schedType"),
        9: FieldParser("labSection"),
        10: FieldParser("phone", ignore_parser),
        11: FieldParser("waitList", bool_parser),
        12: FieldParser("preCheck", bool_parser),
        13: FieldParser("reserved"),
        14: FieldParser("attr"),
        15: FieldParser("creditHours"),
        16: FieldParser("billHours"),
        17: FieldParser("instructor", instructor_parser),
    }

    def __init__(self):
        #        "                                                     *** DAYS ***  BEG  END          SCHED  ASSOC LAB/      WAIT PRE RESV       CRED BILL                                 "
        #        "                 COURSE               SEC CRN   SLOT M T W R F S U TIME TIME  ROOM   TYPE   LEC SECT   PHON LIST CHK LFTD ATTR   HR   HR  INSTRUCTOR                      "
        #        "                 ------               --- ----- ---- ------------- ---- ---- ------- -----  ---------- ---- ---- --- ---- ----- ---- ---- ----------                      "
        legend = "------------------------------------- --- ----- ---- ------------- ---- ---- ------- ------ ---------- ---- ---- --- ---- ----- ---- ---- --------------------------------"
        sections = legend.split(" ")
        self.sections = list(map(lambda s: len(s), sections))

    def parse(self, raw_course):
        data = {}
        last = 0
        for index, section in enumerate(self.sections):
            location = last + section + 1

            current_data = raw_course[last:location]

            cp = CourseParser.index_map[index]
            parsed_data = cp.parse(current_data)

            if parsed_data != None:
                data[cp.name] = parsed_data

            last = location
            raw_course.replace(current_data, "")
        return data


course_parser = CourseParser()


def parse_entire_list():
    response = grab_entire_resp()
    soup = BeautifulSoup(response.text, "html.parser")

    data = {"semester": soup.body.h2.text, "courses": []}

    pre = soup.body.pre.text

    contents = pre.split("Subject: ")

    for entry in contents:
        content = list(map(lambda s: s.strip(), entry.split("\n")))
        content = [x for x in content if x]

        subject = content[0]
        content.pop(0)

        for line in content:
            if CourseParser.course_name_regex.match(line[:9]):
                course = course_parser.parse(line)
                data["courses"].append(course)

    return data


@app.route("/")
def get_entire_list():
    return jsonify(parse_entire_list())


if __name__ == "__main__":
    for course in parse_entire_list()["courses"]:
        print(course)
