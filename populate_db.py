from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import muntrunk.db
from muntrunk.parse import parse_entire_list

Base = declarative_base()
engine = create_engine(
    "postgresql://postgres:superGoodPassword@localhost:5432/muntrunk"
)
Session = sessionmaker(bind=engine)
session = Session()


class Semester(Base):
    __tablename__ = "semesters"
    id = Column(Integer, primary_key=True)
    title = Column(String)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    semester = relationship("Semester")
    subject = Column(String)
    number = Column(String)
    name = Column(String)


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course")
    crn = Column(Integer)
    primary_instructor = Column(String)
    secondary_instructor = Column(String)
    wait_list = Column(Boolean)
    pre_check = Column(Boolean)
    schedule_type = Column(String)
    credit_hours = Column(Integer)
    billed_hours = Column(Integer)


class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.id"))
    section = relationship("Section")
    days_of_week = Column(ARRAY(String))
    begin = Column(Integer)
    end = Column(Integer)
    building = Column(String)
    room = Column(String)


Base.metadata.create_all(engine)

semester = parse_entire_list()


def without_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}


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
