import os
import logging

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

logger = logging.getLogger(__name__)

Base = declarative_base()


def db_drop_all():
    logger.debug("dropping all")
    with engine.connect() as con:
        con.execute("DROP SCHEMA public CASCADE")
        con.execute("CREATE SCHEMA public")


@dataclass
class CommonDBTypes:
    campuses: dict
    instructors: dict
    buildings: dict
    rooms: dict
    sessions: dict
    subjects: dict


common_db_types = CommonDBTypes(
    campuses={}, instructors={}, buildings={}, rooms={}, sessions={}, subjects={},
)


class Building(Base):
    __tablename__ = "building"
    id = Column(Integer, primary_key=True)
    letter = Column(String)
    campus_id = Column(Integer, ForeignKey("campus.id"))
    campus = relationship("Campus")


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    number = Column(String)
    building_id = Column(Integer, ForeignKey("building.id"))
    building = relationship("Building")


class Instructor(Base):
    __tablename__ = "instructor"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Campus(Base):
    __tablename__ = "campus"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Semester(Base):
    __tablename__ = "semester"
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    term = Column(Integer)
    level = Column(Integer)


class Session(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    semester_id = Column(Integer, ForeignKey("semester.id"))
    semester = relationship("Semester", foreign_keys=[semester_id])
    campus_id = Column(Integer, ForeignKey("campus.id"))
    campus = relationship("Campus", foreign_keys=[campus_id])
    session_id = Column(Integer, ForeignKey("session.id"))
    session = relationship("Session", foreign_keys=[session_id])
    subject_id = Column(Integer, ForeignKey("subject.id"))
    subject = relationship("Subject", foreign_keys=[subject_id])
    number = Column(String)
    name = Column(String)
    meta = Column(ARRAY(String))


class Section(Base):
    __tablename__ = "section"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    course = relationship("Course", foreign_keys=[course_id])
    crn = Column(Integer)
    primary_instructor_id = Column(Integer, ForeignKey("instructor.id"))
    primary_instructor = relationship(
        "Instructor", foreign_keys=[primary_instructor_id]
    )
    secondary_instructor_id = Column(Integer, ForeignKey("instructor.id"))
    secondary_instructor = relationship(
        "Instructor", foreign_keys=[secondary_instructor_id]
    )
    wait_list = Column(Boolean)
    pre_check = Column(Boolean)
    schedule_type = Column(String)
    lab_sections = Column(ARRAY(Integer))
    credit_hours = Column(Integer)
    billed_hours = Column(Integer)
    meta = Column(ARRAY(String))


class Slot(Base):
    __tablename__ = "slot"
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("section.id"))
    section = relationship("Section", foreign_keys=[section_id])
    days_of_week = Column(ARRAY(String))
    begin = Column(Integer)
    end = Column(Integer)
    building_id = Column(Integer, ForeignKey("building.id"))
    building = relationship("Building", foreign_keys=[building_id])
    room_id = Column(Integer, ForeignKey("room.id"))
    room = relationship("Room", foreign_keys=[room_id])
    meta = Column(ARRAY(String))


engine = create_engine(os.getenv("HASURA_GRAPHQL_DATABASE_URL"))


def init_tables():
    Base.metadata.create_all(engine)


init_tables()

SqlSession = sessionmaker(bind=engine)
session = SqlSession()
