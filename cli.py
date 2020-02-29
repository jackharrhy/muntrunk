from dotenv import load_dotenv

load_dotenv()

import logging
import click
from muntrunk.types import Semester, common_types
from muntrunk.data import fetch_all_semesters, fetch_semester
from muntrunk.db import Building, Room, Instructor, Campus, Semester, Course, Section, Slot, session, engine, common_db_types
from muntrunk.utils import without_keys

logging.basicConfig(level=logging.DEBUG)


@click.group()
def cli():
    pass


@cli.command()
def db_populate_all():
    all_semesters = list(fetch_all_semesters)

    for semester in fetch_all_semesters():
        sql_semester = Semester(**without_keys(semester.dict(), ["courses"]))

        for course in semester.courses:
            sql_course = Course(**without_keys(course.dict(), ["sections"]))
            sql_course.semester = sql_semester

            for section in course.sections:
                sql_section = Section(**without_keys(section.dict(), ["slots"]))
                sql_section.course = sql_course

                for slot in section.slots:
                    sql_slot = Slot(**slot.dict())
                    sql_slot.section = sql_section
                    session.add(sql_slot)

                session.add(sql_section)

            session.add(sql_course)

        session.add(sql_semester)

    session.commit()
    session.close()


@cli.command()
def db_drop_all():
    with engine.connect() as con:
        con.execute('DROP SCHEMA public CASCADE')
        con.execute('CREATE SCHEMA public')


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
