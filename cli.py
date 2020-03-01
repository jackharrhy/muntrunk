from dotenv import load_dotenv

load_dotenv()

import logging
import click
from muntrunk.types import Semester, common_types
from muntrunk.data import fetch_all_semesters, fetch_semester
from muntrunk.db import (
    Building,
    Room,
    Instructor,
    Campus,
    Semester,
    Course,
    Section,
    Slot,
    session,
    engine,
    common_db_types,
)
from muntrunk.utils import without_keys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


def db_populate_semester(semester, session):
    logger.debug(
        f"populating semester: {semester.year}_{semester.term}_{semester.level}"
    )
    semester_stripped = without_keys(semester.dict(), ["courses"])
    sql_semester = Semester(**semester_stripped)
    session.add(sql_semester)

    for course in semester.courses:
        course_stripped = without_keys(course.dict(), ["campus", "sections"])
        sql_course = Course(**course_stripped)
        sql_course.campus = common_db_types.campuses[course.campus.name]
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


@cli.command()
def db_populate_all():
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

    for semester in all_semesters:
        db_populate_semester(semester, session)

    session.commit()
    session.close()


@cli.command()
def db_drop_all():
    with engine.connect() as con:
        con.execute("DROP SCHEMA public CASCADE")
        con.execute("CREATE SCHEMA public")


@cli.command()
@click.option("--year", default=2019)
@click.option("--term", default=2)
@click.option("--level", default=1)
@click.option("--onlytypes", default=False)
def jsondump_semester(year, term, level, onlytypes):
    logging.disable(logging.DEBUG)
    all_semesters = fetch_semester(year, term, level)
    if not onlytypes:
        print(all_semesters.json())
    else:
        print(common_types.json())


@cli.command()
def jsondump_all():
    logging.disable(logging.DEBUG)
    print(fetch_all_semesters().json())


if __name__ == "__main__":
    cli()
