from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, List, Optional


@dataclass
class CommonTypes:
    campuses: dict
    instructors: dict
    buildings: dict
    rooms: dict


common_types = CommonTypes(campuses={}, instructors={}, buildings={}, rooms={},)


class Building(BaseModel):
    letter: str

    def grab(letter):
        if not letter:
            return None

        if not letter in common_types.buildings:
            new_building = Building(letter=letter)
            common_types.buildings[letter] = new_building
            return new_building
        else:
            return common_types.buildings[letter]


class Room(BaseModel):
    building: Building
    number: str

    def grab(building, number):
        if not building:
            return None

        if not number in common_types.rooms:
            new_room = Room(building=building, number=number)
            common_types.rooms[number] = new_room
            return new_room
        else:
            return common_types.rooms[number]


class Instructor(BaseModel):
    name: str

    def grab(name):
        if not name:
            return None

        if not name in common_types.instructors:
            new_instructor = Instructor(name=name)
            common_types.instructors[name] = new_instructor
            return new_instructor
        else:
            return common_types.instructors[name]


class Campus(BaseModel):
    name: str

    def grab(name):
        if not name:
            return None

        if not name in common_types.campuses:
            new_campus = Campus(name=name)
            common_types.campuses[name] = new_campus
            return new_campus
        else:
            return common_types.campuses[name]


class Slot(BaseModel):
    days_of_week: List[str]
    begin: Optional[int]
    end: Optional[int]
    building: Optional[Building]
    room: Optional[Room]

    def from_piece(piece):
        building = Building.grab(piece["room"]["building"])
        room = Room.grab(building, piece["room"]["room"])

        return Slot(
            days_of_week=piece["days"],
            begin=piece["begin"],
            end=piece["end"],
            building=building,
            room=room,
        )


class Section(BaseModel):
    crn: int
    primary_instructor: Optional[Instructor]
    secondary_instructor: Optional[Instructor]
    wait_list: bool
    pre_check: bool
    schedule_type: Optional[str]
    credit_hours: int
    billed_hours: Optional[int]
    slots: List[Slot]

    def from_piece(piece):
        primary_instructor = Instructor.grab(piece["instructor"]["primary"])
        secondary_instructor = Instructor.grab(piece["instructor"]["secondary"])

        return Section(
            crn=piece["crn"],
            primary_instructor=primary_instructor,
            secondary_instructor=secondary_instructor,
            wait_list=piece["waitList"],
            pre_check=piece["preCheck"],
            schedule_type=piece["schedType"],
            credit_hours=piece["creditHours"],
            billed_hours=piece["billHours"],
            slots=[],
        )


class Course(BaseModel):
    campus: Campus
    session: str
    subject: str
    number: str
    name: Optional[str]
    sections: List[Section]

    def from_piece(piece):
        campus = Campus.grab(piece["campus"])

        return Course(
            campus=campus,
            session=piece["session"],
            subject=piece["course"]["subject"],
            number=piece["course"]["number"],
            name=piece["course"]["name"],
            sections=[],
        )


class Semester(BaseModel):
    year: int
    term: int
    level: int
    courses: List[Course]


@dataclass
class Types:
    course: Any = None
    section: Any = None
    slot: Any = None


def types_from_piece(valid, piece):
    types = Types(None, None, None)

    if valid.course:
        types.course = Course.from_piece(piece)

    contains_time = valid.begin and valid.end

    is_on_campus = contains_time and (
        valid.crn or valid.schedule or valid.days_of_the_week
    )
    is_online = piece["slot"] == 99
    is_edge_case_but_valid = valid.crn and valid.schedule

    if is_on_campus or is_online or is_edge_case_but_valid:
        if valid.crn:
            types.section = Section.from_piece(piece)

            if valid.course:
                types.course.sections.append(types.section)

        if valid.days_of_the_week:
            types.slot = Slot.from_piece(piece)

            if types.section:
                types.section.slots.append(types.slot)

    if not types.course and not types.section and not types.slot:
        return None

    return types
