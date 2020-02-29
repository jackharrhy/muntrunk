import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


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


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    semester_id = Column(Integer, ForeignKey("semester.id"))
    semester = relationship("Semester")
    campus_id = Column(Integer, ForeignKey("campus.id"))
    campus = relationship("Campus")
    session = Column(String)
    subject = Column(String)
    number = Column(String)
    name = Column(String)


class Section(Base):
    __tablename__ = "section"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    course = relationship("Course")
    crn = Column(Integer)
    primary_instructor_id = Column(Integer, ForeignKey("instructor.id"))
    primary_instructor = relationship("Instructor")
    secondary_instructor_id = Column(Integer, ForeignKey("instructor.id"))
    secondary_instructor = relationship("Instructor")
    wait_list = Column(Boolean)
    pre_check = Column(Boolean)
    schedule_type = Column(String)
    credit_hours = Column(Integer)
    billed_hours = Column(Integer)


class Slot(Base):
    __tablename__ = "slot"
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("section.id"))
    section = relationship("Section")
    days_of_week = Column(ARRAY(String))
    begin = Column(Integer)
    end = Column(Integer)
    building_id = Column(Integer, ForeignKey("building.id"))
    building = relationship("Building")
    room_id = Column(Integer, ForeignKey("room.id"))
    room = relationship("Room")


engine = create_engine(os.getenv("POSTGRES_HOST_DATABASE_URL"))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
