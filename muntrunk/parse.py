import re
from dataclasses import dataclass
from bs4 import BeautifulSoup
from .types import Semester, Course, Section, Slot, types_from_piece


class FieldParser:
    def __init__(self, name, parse_function="default_parser"):
        self.name = name
        self.parse_function = parse_function


class InvalidPiece(Exception):
    pass


known_garbage_lines = [
    "                                                     *** DAYS ***  BEG  END          SCHED  ASSOC LAB/      WAIT PRE RESV       CRED BILL                                 ",
    "                 COURSE               SEC CRN   SLOT M T W R F S U TIME TIME  ROOM   TYPE   LEC SECT   PHON LIST CHK LFTD ATTR   HR   HR  INSTRUCTOR                      ",
    "                 ------               --- ----- ---- ------------- ---- ---- ------- -----  ---------- ---- ---- --- ---- ----- ---- ---- ----------                      ",
]


class Piece(dict):
    legend = "------------------------------------- --- ----- ---- ------------- ---- ---- ------- ------ ---------- ---- ---- --- ---- ----- ---- ---- --------------------------------"
    course_name_regex = re.compile("([A-Z])([A-Z]| ){3} (\d|[A-Z]){4}")
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
        "WWW",
    ]

    @dataclass
    class Valid:
        room: bool = True
        course: bool = True
        crn: bool = True
        slot: bool = True
        days_of_the_week: bool = True
        begin: bool = True
        end: bool = True
        schedule: bool = True
        lab_sections: bool = True

    def default_parser(self, field):
        field = field.strip()

        if field == "":
            return None

        try:
            return int(field)
        except ValueError:
            return field

    def potential_na_parser(self, field):
        value = self.default_parser(field)

        if value == "NA":
            return None
        else:
            return value

    def crn_parser(self, field):
        if len(field.strip()) != 5:
            self.valid.crn = False
            return None

        try:
            return int(field)
        except ValueError:
            self.valid.crn = False

    def slot_parser(self, field):
        try:
            return int(field)
        except ValueError:
            self.valid.slot = False

    def begin_parser(self, field):
        try:
            return int(field)
        except ValueError:
            self.valid.begin = False

    def end_parser(self, field):
        try:
            return int(field)
        except ValueError:
            self.valid.end = False

    def schedule_parser(self, field):
        field = field.strip()
        if field in self.known_schedule_values:
            return field
        else:
            self.valid.schedule = False

    def lab_sections_parser(self, field):
        field = field.strip()

        if field == "":
            if self:
                self.valid.lab_section = False
            return []

        lab_sections = []

        pieces = field.split(" ")
        for value in pieces:
            if len(value) != 3:
                if self:
                    self.valid.lab_section = False
                return []

            try:
                lab_sections.append(int(value))
            except ValueError:
                if self:
                    self.valid.lab_section = False
                return []

        return lab_sections

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
            return None

    def ignore_parser(self, field):
        return None

    def days_of_the_week_parser(self, field):
        fields = field.strip().split(" ")
        fields = [x for x in fields if x]

        if len(fields) == 0:
            self.valid.days_of_the_week = False
            return []

        for field in fields:
            if not field in Piece.valid_days_of_the_week:
                self.valid.days_of_the_week = False

        return fields

    # silly edgecase where the session name refers to the course, with no course listed
    course_name_in_session_regex = re.compile(
        "((?P<subject>[A-Z]*) (?P<number>\d{4})-(?P<section>\d{3}))+"
    )

    def course_name_parser(self, field):
        if not Piece.course_name_regex.match(self.raw_course[:9]):
            if self.session:
                potential_match = Piece.course_name_in_session_regex.match(self.session)

                if potential_match:
                    self.course_name_in_session = True
                    groups = potential_match.groupdict()
                    for k in groups:
                        groups[k] = groups[k].strip()
                    return {
                        "subject": groups["subject"].strip(),
                        "number": groups["number"].strip(),
                        "name": None,
                    }

            self.partial = True
            self.valid.course = False

        stripped = field.strip()
        if stripped == "":
            return None

        return {
            "subject": field[:4].strip(),
            "number": field[5:9].strip(),
            "name": field[10:].strip(),
        }

    def instructor_parser(self, field):
        parts = field.split(" - ")
        if len(parts) != 2:
            return {"primary": None, "secondary": None}
        else:
            if len(parts[1].strip()) > 18:
                return {
                    "primary": parts[1][:14].strip(),
                    "secondary": parts[1][14:].strip(),
                }
            else:
                return {"primary": parts[1].strip(), "secondary": None}

    room_regex = re.compile(
        "(?P<building>([A-Z])([A-Z]| ){2})(?P<room>(\d){4}([A-Z])?)"
    )

    def room_parser(self, field):
        field = field.strip()
        if field == "":
            self.valid.room = False
            return {"building": None, "room": None}

        potential_match = Piece.room_regex.match(field)
        if potential_match:
            groups = potential_match.groupdict()
            for k in groups:
                groups[k] = groups[k].strip()
            return groups
        else:
            self.valid.room = False
            return {"building": None, "room": None}

    index_map = {
        0: FieldParser("course", "course_name_parser"),
        1: FieldParser("section"),
        2: FieldParser("crn", "crn_parser"),
        3: FieldParser("slot", "slot_parser"),
        4: FieldParser("days", "days_of_the_week_parser"),
        5: FieldParser("begin", "begin_parser"),
        6: FieldParser("end", "end_parser"),
        7: FieldParser("room", "room_parser"),
        8: FieldParser("schedType", "schedule_parser"),
        9: FieldParser("labSections", "lab_sections_parser"),
        10: FieldParser("phone", "ignore_parser"),
        11: FieldParser("waitList", "bool_parser"),
        12: FieldParser("preCheck", "bool_parser"),
        13: FieldParser("reserved", "bool_parser"),
        14: FieldParser("attr"),
        15: FieldParser("creditHours"),
        16: FieldParser("billHours", "potential_na_parser"),
        17: FieldParser("instructor", "instructor_parser"),
    }

    def __init__(self, raw_course, campus, session, *args, **kwargs):
        super(Piece, self).__init__(*args, **kwargs)

        self["campus"] = campus

        self.session = session
        self["session"] = session

        self.partial = False
        self.course_name_in_session = False
        self.raw_course = raw_course
        self.valid = Piece.Valid()

        sections = Piece.legend.split(" ")
        self.sections = list(map(lambda s: len(s), sections))

        self["source"] = raw_course
        self.parse(raw_course)

    def parse(self, raw_course):
        last = 0
        for index, section in enumerate(self.sections):
            location = last + section + 1

            current_data = raw_course[last:location]

            cp = Piece.index_map[index]
            parsed_data = getattr(self, cp.parse_function)(current_data)

            self[cp.name] = parsed_data

            last = location
            raw_course.replace(current_data, "")

        if self.course_name_in_session:
            if (not self.valid.crn) and (not self.valid.schedule):
                self.valid.course = False

        types = types_from_piece(self.valid, self)

        if not types:
            raise InvalidPiece(f"{str(vars(self.valid))} - {raw_course}")

        self["types"] = types


def parse_semester(response, year, term, level):
    soup = BeautifulSoup(response.text, "html.parser")

    semester = Semester(year=year, term=term, level=level, courses=[])

    pre = soup.body.pre.text

    contents = pre.split("Subject: ")

    campus = None
    session = None

    for entry in contents:
        content = entry.split("\n")
        content = [x for x in content if x]

        subject = content[0].strip()

        content.pop(0)

        last_course = None
        last_section = None

        for line in content:
            if line in known_garbage_lines:
                continue

            try:
                piece = Piece(line, campus, session)
                types = piece["types"]

                if types.course:
                    if last_course:
                        semester.courses.append(last_course)
                        last_course = None
                        last_section = None

                    last_course = types.course

                    if len(types.course.sections) > 0:
                        last_section = types.course.sections[0]

                elif types.section:
                    if last_course:
                        last_course.sections.append(types.section)
                    else:
                        # NURS 4512 is quite odd
                        semester.courses[-1].sections.append(types.section)
                    last_section = types.section

                elif types.slot:
                    last_section.slots.append(types.slot)

                continue
            except InvalidPiece:
                pass

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

                meta = []

                if might_by_empty == "":
                    # TODO handle major / minor meta

                    potential_lab_sections = Piece.lab_sections_parser(
                        None, remaining_data[50:].strip()
                    )
                    if len(potential_lab_sections) > 0:
                        types.section.lab_sections.extend(potential_lab_sections)

                    continue

                reserved_for = "RESERVED  FOR:"
                cross_listed = "CROSS LISTED:"
                available_to = "AVAILABLE  TO:"
                not_available_to = "NOT AVAILABLE TO:"

                remaining_data = remaining_data.strip()

                if remaining_data.startswith(reserved_for):
                    meta.append(
                        f"Reserved For: {remaining_data[len(reserved_for):].strip()}"
                    )
                elif remaining_data.startswith(cross_listed):
                    meta.append(
                        f"Cross-listed: {remaining_data[len(cross_listed):].strip()}"
                    )
                elif remaining_data.startswith(available_to):
                    meta.append(
                        f"Available To: {remaining_data[len(available_to):].strip()}"
                    )
                elif remaining_data.startswith(not_available_to):
                    meta.append(
                        f"Not Available To: {remaining_data[len(not_available_to):].strip()}"
                    )
                else:
                    meta.append(remaining_data)

                if types.section:
                    types.section.meta.append(meta)
                elif types.slot:
                    types.slot.meta.append(meta)
                elif types.course:
                    types.course.meta.append(meta)
                else:
                    raise Exception("No slot to put meta into!")

        if last_course:
            semester.courses.append(last_course)

    return semester
