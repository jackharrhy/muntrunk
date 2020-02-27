from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, List, Optional


class Slot(BaseModel):
    days_of_week: List[str]
    begin: Optional[int]
    end: Optional[int]
    building: Optional[str]
    room: Optional[str]

    def from_piece(piece):
        return Slot(
            days_of_week=piece["days"],
            begin=piece["begin"],
            end=piece["end"],
            building=piece["room"]["building"],
            room=piece["room"]["room"],
        )


class Section(BaseModel):
    crn: int
    primary_instructor: Optional[str]
    secondary_instructor: Optional[str]
    wait_list: bool
    pre_check: bool
    schedule_type: Optional[str]
    credit_hours: int
    billed_hours: Optional[int]
    slots: List[Slot]

    def from_piece(piece):
        return Section(
            crn=piece["crn"],
            primary_instructor=piece["instructor"]["primary"],
            secondary_instructor=piece["instructor"]["secondary"],
            wait_list=piece["waitList"],
            pre_check=piece["preCheck"],
            schedule_type=piece["schedType"],
            credit_hours=piece["creditHours"],
            billed_hours=piece["billHours"],
            slots=[],
        )


class Course(BaseModel):
    campus: str
    session: str
    subject: str
    number: str
    name: Optional[str]
    sections: List[Section]

    def from_piece(piece):
        return Course(
            campus=piece["campus"],
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
