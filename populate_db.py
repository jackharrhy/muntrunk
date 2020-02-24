from muntrunk.db import Semester, Course, Section, Slot, session
from muntrunk.parse import parse_w2020
from muntrunk.utils import without_keys

semester = parse_w2020()

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