import json
import sqlite3

try:
    con = sqlite3.connect('SchoolScheduler.db')
    cur = con.cursor()
except sqlite3.Error as e:
    print(e)

def db_init():
    cur.execute('''CREATE TABLE IF NOT EXISTS Students (id integer PRIMARY KEY, first text, last text, gpa real)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Classes (id integer, class text)''')
    con.commit()


def db_close():
    con.close()


def get_students():
    students = cur.execute("SELECT * FROM Students").fetchall()
    print(json.dumps(students))


def insert_student(student_id, f_name, l_name, grade):
    cur.execute(f'INSERT INTO Students VALUES ({student_id},"{f_name}", "{l_name}", {grade})')
    con.commit()


def get_classes():
    classes = cur.execute("SELECT * FROM Classes").fetchall()
    print(json.dumps(classes))


def insert_class(student_id, class_name):
    cur.execute(f'INSERT INTO Classes VALUES ({student_id}, "{class_name}")')
    con.commit()


def delete_all():
    con.execute("DELETE FROM Students")
    con.execute("DELETE FROM Classes")
