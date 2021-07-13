from sqlalchemy import Column, ForeignKey, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json


Base = declarative_base()
engine = create_engine('sqlite:///SchoolScheduler.db')

#drop and recreate all tables
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Student(Base):
    __tablename__ = 'Student'
    id = Column(Integer, primary_key=True)
    first = Column(String(250), nullable=False)
    last = Column(String(250), nullable=False)
    gpa = Column(Integer, nullable=False)

    @staticmethod
    def get_all():
        query = session.query(Student)
        return session.execute(query).all()

    @staticmethod
    def by_id(id):
        query = session.query(Student).where(Student.id == id)
        return session.execute(query).scalar()

    @staticmethod
    def insert(id, first, last, gpa):
        session.add(Student(id=id, first=first, last=last, gpa=gpa))
        session.commit()

class Class(Base):
    __tablename__ = 'Class'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('Course.id'))
    period = Column(Integer, nullable=False)

    @staticmethod
    def get_all():
        query = session.query(Class)
        return session.execute(query).all()

    @staticmethod
    def by_id(id):
        query = session.query(Classes).where(Class.id == id)
        return session.execute(query).scalar()


class Course(Base):
    __tablename__ = 'Course'
    id = id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)
    capacity = Column(Integer, nullable=False)


class Schedule(Base):
    __tablename__ = "Schedule"

    id = Column(Integer, primary_key=True)
    session = Column(Integer, ForeignKey('Class.id'))
    student = Column(Integer, ForeignKey('Student.id'))


class Preference(Base):
    __tablename__ = "Preference"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('Course.id'))
    student_id = Column(Integer, ForeignKey('Student.id'))
    period = Column(Integer, nullable=False)


class Class_History(Base):
    __tablename__ = "Class_History"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Student.id'))
    class_name = Column(String(250), nullable=False)
    credit = Column(Integer, nullable=False)
    grade = Column(String(250), nullable=False)


def db_init():
    Base.metadata.create_all(engine)


def db_purge():
    Base.metadata.drop_all(engine)


db_purge()
db_init()

scheduled_class = Schedule(session=1, student=1)
session.add(scheduled_class)
session.add(Student(id=2, first="Test",last="Name",gpa=3.0))
session.commit()

classes = session.query(Class).all()
students = session.query(Student).all()
schedules = session.query(Schedule).all()

print(schedules[0].student)

s = Student.by_id(2)
print(s.first)
s.first = "aaaa"
print(Student.by_id(2).first)

for student in students:
    print(str(student.id) + " " + student.first)

for scheduled_class in classes:
    print(scheduled_class.name)
