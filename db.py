import json
import sqlite3

try:
    con = sqlite3.connect('SchoolScheduler.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
except sqlite3.Error as e:
    print(e)

def db_init():
    cur.execute('''CREATE TABLE IF NOT EXISTS Students (id integer PRIMARY KEY, first text, last text, gpa real)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Classes (id integer, name text, period integer, capacity integer)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Schedules (class_id integer, student_id integer, period integer)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Preferences (class_id integer, student_id integer, period integer)''')
    con.commit()


def db_close():
    con.close()


def to_dict(query_out):
    dict_arr = []
    for i in query_out:
        dict_arr.append(dict(i))
    return dict_arr

def get_students():
    students = cur.execute("SELECT * FROM Students").fetchall()
    return to_dict(students)


def insert_student(student_id, f_name, l_name, grade):
    cur.execute(f'INSERT INTO Students VALUES ({student_id},"{f_name}", "{l_name}", {grade})')
    con.commit()


def get_classes():
    classes = cur.execute("SELECT * FROM Classes").fetchall()
    return to_dict(classes)


def get_classes_id_period(class_id, period):
    classes = cur.execute(f"SELECT * FROM Classes WHERE id = {class_id} AND period = {period}").fetchone()
    return dict(classes)


def insert_class(student_id, class_name, period, capacity = 15):
    cur.execute(f'INSERT INTO Classes VALUES ({student_id}, "{class_name}", {period}, {capacity})')
    con.commit()


def insert_schedule(class_id, student_id, period):
    cur.execute(f'INSERT INTO Schedules VALUES ({class_id}, {student_id}, {period})')
    con.commit()


def get_schedules():
    schedules = cur.execute("SELECT * FROM Schedules").fetchall()
    return to_dict(schedules)

def get_schedules_student(student_id):
    schedules = cur.execute(f"SELECT * FROM Schedules WHERE student_id = {student_id}").fetchall()
    return to_dict(schedules)

def insert_preference(class_id, student_id, period):
    cur.execute(f'INSERT INTO Preferences VALUES ({class_id}, {student_id}, {period})')
    con.commit()


def get_preferences():
    preferences = cur.execute("SELECT * FROM Preferences").fetchall()
    return to_dict(preferences)


def get_preferences_period(period):
    preferences = cur.execute(f"SELECT * FROM Preferences WHERE period = {period}").fetchall()
    return to_dict(preferences)


def course_available(course_id, student_id, period):
    course = cur.execute(f'SELECT * FROM Classes WHERE id = {course_id} AND period = {period} LIMIT 1').fetchone()
    if (len(course) < 1):
        return False
    capacity = course['capacity']
    enrolled_count = cur.execute(f'SELECT Count(*) FROM Schedules WHERE class_id = {course_id} AND student_id = {student_id} AND period = {period}').fetchone()[0]
    if enrolled_count >= capacity:
        return False
    return True

def delete_all():
    con.execute("DELETE FROM Students")
    con.execute("DELETE FROM Classes")
    con.execute("DELETE FROM Preferences")
    con.execute("DELETE FROM Schedules")
