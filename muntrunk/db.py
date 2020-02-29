import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


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
    campus = Column(String)
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
    primary_instructor = Column(String)
    secondary_instructor = Column(String)
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
    building = Column(String)
    room = Column(String)


engine = create_engine(os.getenv("POSTGRES_HOST_DATABASE_URL"))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
