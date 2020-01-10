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


class FieldParser:
    def __init__(self, name, parse_function="default_parser"):
        self.name = name
        self.parse_function = parse_function


class InvalidCourse(Exception):
    pass


known_garbage_lines = [
    "                                                     *** DAYS ***  BEG  END          SCHED  ASSOC LAB/      WAIT PRE RESV       CRED BILL                                 ",
    "                 COURSE               SEC CRN   SLOT M T W R F S U TIME TIME  ROOM   TYPE   LEC SECT   PHON LIST CHK LFTD ATTR   HR   HR  INSTRUCTOR                      ",
    "                 ------               --- ----- ---- ------------- ---- ---- ------- -----  ---------- ---- ---- --- ---- ----- ---- ---- ----------                      ",
]


class Course(dict):
    legend = "------------------------------------- --- ----- ---- ------------- ---- ---- ------- ------ ---------- ---- ---- --- ---- ----- ---- ---- --------------------------------"
    course_name_regex = re.compile("([A-Z]){3}([A-Z]| ) (\d|[A-Z]){4}")
    valid_days_of_the_week = ["M", "T", "W", "R", "F", "S", "U"]
    known_schedule_values = [
        "LEC",
        "SEM",
        "HES",
        "L&L",
        "DST",
        "WRK",
        "IND",
        "LAB",
        "CLI",
        "INT",
        "REA",
        "CEX",
    ]

    class Valid:
        def __init__(self):
            self.course = True
            self.crn = True
            self.slot = True
            self.days_of_the_week = True
            self.begin = True
            self.end = True
            self.schedule = True

    def default_parser(self, field):
        field = field.strip()

        if field == "":
            return None

        try:
            return self.int_parser(field)
        except ValueError:
            return field

    def int_parser(self, field):
        return int(field)

    def crn_parser(self, field):
        try:
            return self.int_parser(field)
        except ValueError:
            self.valid.crn = False

    def slot_parser(self, field):
        try:
            return self.int_parser(field)
        except ValueError:
            self.valid.slot = False

    def begin_parser(self, field):
        try:
            return self.int_parser(field)
        except ValueError:
            self.valid.begin = False

    def end_parser(self, field):
        try:
            return self.int_parser(field)
        except ValueError:
            self.valid.end = False

    def schedule_parser(self, field):
        field = field.strip()
        if field in self.known_schedule_values:
            return field
        else:
            self.valid.schedule = False

    def bool_parser(self, field):
        field = field.strip()
        if field == "":
            return None
        fields = field.split(" ")
        if len(fields) == 1:
            return bool(fields[0])
        elif len(fields) == 2:
            return [bool(fields[0]), bool(fields[1])]
        else:
            raise "found a boolean field with > 2 fields!"

    def ignore_parser(self, field):
        return None

    def days_of_the_week_parser(self, field):
        fields = field.strip().split(" ")
        fields = [x for x in fields if x]

        if len(fields) == 0:
            self.valid.days_of_the_week = False

        for field in fields:
            if not field in Course.valid_days_of_the_week:
                self.valid.days_of_the_week = False

        return fields

    def course_name_parser(self, field):
        if not Course.course_name_regex.match(self.raw_course[:9]):
            self.partial = True
            self.valid.course = False

        stripped = field.strip()
        if stripped == "":
            return None

        return {"subject": field[:4], "number": field[5:9], "name": field[10:].strip()}

    # TODO parse multiple instructors per course
    def instructor_parser(self, field):
        parts = field.split(" - ")
        if len(parts) != 2:
            return None
        else:
            return {"type": parts[0].strip(), "name": parts[1].strip()}

    index_map = {
        0: FieldParser("course", "course_name_parser"),
        1: FieldParser("section"),
        2: FieldParser("crn", "crn_parser"),
        3: FieldParser("slot", "slot_parser"),
        4: FieldParser("days", "days_of_the_week_parser"),
        5: FieldParser("begin", "begin_parser"),
        6: FieldParser("end", "end_parser"),
        7: FieldParser("room"),  # TODO parse one char room names
        8: FieldParser("schedType", "schedule_parser"),
        9: FieldParser("labSection"),
        10: FieldParser("phone", "ignore_parser"),
        11: FieldParser("waitList", "bool_parser"),
        12: FieldParser("preCheck", "bool_parser"),
        13: FieldParser("reserved"),
        14: FieldParser("attr"),
        15: FieldParser("creditHours"),
        16: FieldParser("billHours"),
        17: FieldParser("instructor", "instructor_parser"),
    }

    def __init__(self, raw_course, *args, **kwargs):
        super(Course, self).__init__(*args, **kwargs)

        self.partial = False
        self.raw_course = raw_course
        self.valid = Course.Valid()

        sections = Course.legend.split(" ")
        self.sections = list(map(lambda s: len(s), sections))

        self.parse(raw_course)

    def parse(self, raw_course):
        last = 0
        for index, section in enumerate(self.sections):
            location = last + section + 1

            current_data = raw_course[last:location]

            cp = Course.index_map[index]
            parsed_data = getattr(self, cp.parse_function)(current_data)

            if parsed_data != None:
                self[cp.name] = parsed_data

            last = location
            raw_course.replace(current_data, "")

        if self.valid.course:
            return

        if (
            self.valid.begin
            and self.valid.end
            and (self.valid.crn or self.valid.schedule or self.valid.days_of_the_week)
        ):
            return

        if self.valid.crn and self.valid.slot and self["slot"] == 99:
            return

        raise InvalidCourse(f"{str(vars(self.valid))} - {raw_course}")


def parse_entire_list():
    response = grab_entire_resp()
    soup = BeautifulSoup(response.text, "html.parser")

    data = {"semester": soup.body.h2.text, "courses": []}

    pre = soup.body.pre.text

    contents = pre.split("Subject: ")

    campus = None
    session = None

    for entry in contents:
        content = entry.split("\n")
        content = [x for x in content if x]

        subject = content[0].strip()

        # if subject != "Chemistry":
        #    continue

        content.pop(0)

        for line in content:
            if line in known_garbage_lines:
                continue

            course = None

            try:
                course = Course(line)
                data["courses"].append(course)
                continue
            except InvalidCourse:
                pass

            if course and course.partial:
                pass
                # TODO jam partial_course data into last recorded course
            else:
                if line.startswith("Campus: "):
                    campus = line[8:].strip()
                elif line.startswith("Session: "):
                    session = line[8:].strip()
                else:
                    should_be_empty = line[:42].strip()
                    if should_be_empty != "":
                        if line[35:36] != "  ":
                            # TODO parse date -> date
                            continue
                        else:
                            raise Exception(f"Invalid line: {line}")

                    remaining_data = line[42:]

                    might_by_empty = remaining_data[:15].strip()

                    if might_by_empty == "":
                        # TODO handle MAJOR MINOR tags
                        continue

                    if remaining_data.startswith("RESERVED  FOR: "):
                        pass
                        # TODO handle meta
                    elif remaining_data.startswith("CROSS LISTED: "):
                        pass
                        # TODO handle meta
                    elif remaining_data.startswith("AVAILABLE  TO: "):
                        pass
                        # TODO handle meta
                    elif remaining_data.startswith("NOT AVAILABLE TO: "):
                        pass
                        # TODO handle meta
                    else:
                        pass
                        # TODO handle context-less meta

    return data


@app.route("/")
def get_entire_list():
    return jsonify(parse_entire_list())


if __name__ == "__main__":
    for course in parse_entire_list()["courses"]:
        print(course)
