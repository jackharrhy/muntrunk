from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, List, Optional


@dataclass
class Slot:
    days_of_week: List[str]
    begin: int
    end: int
    building: Optional[str]
    room: Optional[str]

    def from_piece(piece):
        return Slot(
            piece["days"],
            piece["begin"],
            piece["end"],
            piece["room"]["building"],
            piece["room"]["room"],
        )


@dataclass
class Section:
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
            piece["crn"],
            piece["instructor"]["primary"],
            piece["instructor"]["secondary"],
            piece["waitList"],
            piece["preCheck"],
            piece["schedType"],
            piece["creditHours"],
            piece["billHours"],
            [],
        )


@dataclass
class Course:
    subject: str
    number: str
    name: str
    sections: List[Section]

    def from_piece(piece):
        return Course(
            piece["course"]["subject"],
            piece["course"]["number"],
            piece["course"]["name"],
            [],
        )


class Semester(BaseModel):
    semester: str
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
    is_online = valid.crn and valid.slot and piece["slot"] == 99

    if is_on_campus or is_online:
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
