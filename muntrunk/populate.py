import logging

from .types import Semester, common_types
from .data import fetch_all_semesters, fetch_semester
from .db import (
    Building,
    Room,
    Instructor,
    Campus,
    Semester,
    Session,
    Subject,
    Course,
    Section,
    Slot,
    session,
    engine,
    common_db_types,
)
from .utils import without_keys

logger = logging.getLogger(__name__)


def db_populate_semester(semester, session):
    logger.debug(
        f"populating semester: {semester.year}_{semester.term}_{semester.level}"
    )
    semester_stripped = without_keys(semester.dict(), ["courses"])
    sql_semester = Semester(**semester_stripped)
    session.add(sql_semester)

    for course in semester.courses:
        course_stripped = without_keys(
            course.dict(), ["sections", "campus", "session", "subject"]
        )
        sql_course = Course(**course_stripped)
        sql_course.campus = common_db_types.campuses[course.campus.name]
        sql_course.session = common_db_types.sessions[course.session.name]
        sql_course.subject = common_db_types.subjects[course.subject.name]
        sql_course.semester = sql_semester
        session.add(sql_course)

        for section in course.sections:
            section_stripped = without_keys(
                section.dict(), ["slots", "primary_instructor", "secondary_instructor"],
            )
            sql_section = Section(**section_stripped)
            sql_section.course = sql_course
            session.add(sql_section)

            if section.primary_instructor:
                sql_section.primary_instructor = common_db_types.instructors[
                    section.primary_instructor.name
                ]

            if section.primary_instructor:
                sql_section.primary_instructor = common_db_types.instructors[
                    section.primary_instructor.name
                ]

            for slot in section.slots:
                slot_stripped = without_keys(slot.dict(), ["building", "room"])
                sql_slot = Slot(**slot_stripped)
                if slot.building and slot.room:
                    building_key = f"{slot.building.campus.name}_{slot.building.letter}"
                    room_key = f"{building_key}_{slot.room.number}"
                    sql_slot.building = common_db_types.buildings[building_key]
                    sql_slot.room = common_db_types.rooms[room_key]
                sql_slot.section = sql_section
                session.add(sql_slot)


def db_populate_all_semesters():
    all_semesters = dict(fetch_all_semesters())["__root__"]

    logger.debug("generating campuses")
    for campus_name in common_types.campuses:
        sql_campus = Campus(**common_types.campuses[campus_name].dict())
        common_db_types.campuses[campus_name] = sql_campus

    logger.debug("generating buildings")
    for building_key in common_types.buildings:
        building = common_types.buildings[building_key]
        sql_building = Building(**without_keys(building.dict(), ["campus"]))
        sql_building.campus = common_db_types.campuses[building.campus.name]
        common_db_types.buildings[building_key] = sql_building

    logger.debug("generating rooms")
    for room_key in common_types.rooms:
        room = common_types.rooms[room_key]
        sql_room = Room(**without_keys(room.dict(), ["building"]))
        building_key = f"{room.building.campus.name}_{room.building.letter}"
        sql_room.building = common_db_types.buildings[building_key]
        common_db_types.rooms[room_key] = sql_room

    logger.debug("generating instructors")
    for instructor_name in common_types.instructors:
        common_db_types.instructors[instructor_name] = Instructor(
            **common_types.instructors[instructor_name].dict()
        )

    logger.debug("generating sessions")
    for session_name in common_types.sessions:
        common_db_types.sessions[session_name] = Session(
            **common_types.sessions[session_name].dict()
        )

    logger.debug("generating subjects")
    for subject_name in common_types.subjects:
        common_db_types.subjects[subject_name] = Subject(
            **common_types.subjects[subject_name].dict()
        )

    for semester in all_semesters:
        db_populate_semester(semester, session)

    logger.debug("finished population, comitting...")
    session.commit()
    logger.debug("closing session")
    session.close()
