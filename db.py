import json
import sqlite3

con = sqlite3.connect('SchoolScheduler.db')
cur = con.cursor()


def db_init():
    try:
        cur.execute('''CREATE TABLE Students
                       (name text, grade real)''')
    except sqlite3.OperationalError:
        print("Students table already exists")
    con.commit()


def db_close():
    con.close()


def get_students():
    students = cur.execute("SELECT * FROM Students").fetchall()
    print(json.dumps(students))


def insert_student(name, grade):
    cur.execute(f'INSERT INTO Students VALUES ("{name}", 9)')
    con.commit()

