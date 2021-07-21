import random
import sqlite3

try:
    con = sqlite3.connect('SchoolScheduler.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
except sqlite3.Error as e:
    print(e)


def db_init():
    cur.execute('''CREATE TABLE IF NOT EXISTS Students (id integer PRIMARY KEY, first text, last text, gpa real)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Classes (class_id integer, course_id, period integer)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Courses (course_id integer, name text, type text, capacity integer)''')
    # Note that a teacher will also have a schedule as such it is called user_id not just student_id
    cur.execute('''CREATE TABLE IF NOT EXISTS Schedules (user_id integer, class_id integer,period integer)''')

    # Note that Preference period is almost meaningless and is simply here for indexing in UI
    cur.execute('''CREATE TABLE IF NOT EXISTS Preferences (course_id integer, student_id integer, period integer)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Class_History (student_id integer, class text, credit real, grade text)''')
    con.commit()


def db_purge():
    cur.execute('''DROP TABLE IF EXISTS Students''')
    cur.execute('''DROP TABLE IF EXISTS Classes''')
    cur.execute('''DROP TABLE IF EXISTS Courses''')
    cur.execute('''DROP TABLE IF EXISTS Schedules''')
    cur.execute('''DROP TABLE IF EXISTS Preferences''')
    cur.execute('''DROP TABLE IF EXISTS Class_History''')
    con.commit()


def db_close():
    con.close()


def to_dict(query_out):
    dict_arr = []
    for i in query_out:
        dict_arr.append(dict(i))
    return dict_arr

#Students.get_all()
def get_students():
    return cur.execute("SELECT * FROM Students").fetchall()

#Students.by_id()
def get_student(student_id):
    return dict(cur.execute(f"SELECT * FROM Students WHERE id = {student_id}").fetchone())

#Course.get_all()
def get_courses():
    return to_dict(cur.execute("SELECT * FROM Courses").fetchall())

#Student.insert(...)
def insert_student(student_id, f_name, l_name, grade):
    cur.execute(f'INSERT INTO Students VALUES ({student_id},"{f_name}", "{l_name}", {grade})')
    con.commit()

# just modify the student instance
# only handles id, name, and grade as of now
def edit_student(student_id, new_id, f_name, l_name, grade):
    cur.execute("UPDATE Students SET id=?, first=?, last=?, gpa=? WHERE id=?", (new_id, f_name, l_name, grade, student_id))
    con.commit()

# Student.delete()
# deletes student and coursework
def delete_student(student_id):
    cur.execute(f"DELETE FROM Students WHERE id = {student_id}")
    cur.execute(f"DELETE FROM Class_History WHERE student_id = {student_id}")

# Class.get_all()
def get_classes():
    classes = cur.execute("SELECT * FROM Classes").fetchall()
    for c in classes:
        print(dict(c))
    return classes

# Class.get_name()
def get_class_name(class_id):
    course_id = dict(cur.execute(f"SELECT * FROM Classes WHERE class_id = {class_id}").fetchone())
    return dict(cur.execute(f"SELECT * FROM Courses WHERE course_id = {course_id['course_id']}").fetchone())

#Class.insert()
# classes are defined sections of a course such that a course can have multiple sections
def insert_class(class_id, course_id, period):
    cur.execute(f'INSERT INTO Classes VALUES ({class_id},{course_id}, {period})')
    con.commit()

#Schedule.insert()
def insert_schedule(student_id, class_id, period):
    cur.execute(f'INSERT INTO Schedules VALUES ({student_id}, {class_id}, {period})')
    con.commit()

#Course.insert()
# courses are those that a school offers
def insert_course(course_id, course_name, course_type, capacity=15):
    cur.execute(f'INSERT INTO COURSES VALUES ({course_id}, "{course_name}", "{course_type}", {capacity})')
    con.commit()

#Course.by_id(id)
def get_course(course_id):
    return cur.execute(f'SELECT * FROM Courses WHERE course_id = {course_id}').fetchone()

#Schedule.get_all()
def get_schedules():
    return cur.execute("SELECT * FROM Schedules").fetchall()

#Schedule.by_student_id(student)
def get_schedules_student(student_id):
    schedules = cur.execute(f"SELECT * FROM Schedules WHERE user_id = {student_id}").fetchall()
    return to_dict(schedules)

#Preference.insert(...)
# Note that Preference period is almost meaningless and is simply here for indexing in UI
def insert_preference(course_id, student_id, period):
    cur.execute(f'INSERT INTO Preferences VALUES ({course_id}, {student_id}, {period})')
    con.commit()

#Preference.by_id()
def get_preference(student_id):
    return to_dict(cur.execute(f'SELECT * FROM Preferences WHERE student_id = {student_id}').fetchall())

#Preference.get_all()
def get_preferences():
    return to_dict(cur.execute(f'SELECT * FROM Preferences').fetchall())

#Preferences.by_period
def get_preferences_period(period):
    preferences = cur.execute(f"SELECT * FROM Preferences WHERE period = {period}").fetchall()
    return to_dict(preferences)

# Course.available(...)
# TEMP IF COURSE NOT AVAIBLE WE RETURN STUDY HALL
def course_available(course_id, period, student_id):
    classes = cur.execute(f'SELECT * FROM Classes WHERE course_id = {course_id} AND period = {period}').fetchall()
    classes = to_dict(classes)

    for c in classes:
        count = cur.execute(
            f"SELECT Count(*) FROM Schedules WHERE class_id = {c['class_id']} AND period = {period}").fetchone()[0]
        if count < 15:
            return c['class_id']

    return -1

#Student.available(...)
# check if a student has a class during a period
def check_student_available(student_id, period):
    num_in_period = \
        cur.execute(f"SELECT Count(*) FROM Schedules WHERE user_id = {student_id} AND period = {period}").fetchone()[0]
    if num_in_period == 0:
        return True
    return False

#Class_History.insert(...)
def insert_class_history(student_id, name, credit, grade):
    cur.execute(f'INSERT INTO Class_History VALUES ({student_id}, "{name}", {credit}, "{grade}")')
    con.commit()

#Class_History.by_student_id(student_id)
def get_class_history(student_id):
    classes = cur.execute(f"SELECT * FROM Class_History WHERE student_id = {student_id}").fetchall()
    return classes

#Dupe function?
def insert_class_history(student_id, name, credit, grade):
    cur.execute(f'INSERT INTO Class_History VALUES ({student_id}, "{name}", {credit}, "{grade}")')
    con.commit()

#another dupe function?
def get_class_history(student_id):
    classes = cur.execute(f"SELECT * FROM Class_History WHERE student_id = {student_id}").fetchall()
    return classes


def insert_test_students():
    # (id, first, last, GPA)
    words = open('words.txt', 'r')
    lines = words.read().splitlines()

    for x in range(1000):
        insert_student(x, lines[random.randint(0, 10000)], lines[random.randint(0, 10000)], 4)


def insert_test_courses():
    # (name, type)

    # Class ID are generated in order check the UI for easy sorting and dispaly
    courses = [['Algebra 1', 'MATH'],
               ['Algebra 2', 'MATH'],
               ['Geometry', 'MATH'],
               ['ADV MATH 1', 'MATH'],
               ['ADV MATH 2', 'MATH'],
               ['ELA 1', 'ELA'],
               ['ELA 2', 'ELA'],
               ['ELA 3', 'ELA'],
               ['ELA 4', 'ELA'],
               ['Biology 1', 'SCIENCE'],
               ['Science Class 1', 'SCIENCE'],
               ['Science Class 2', 'SCIENCE'],
               ['World History', 'SOCIAL'],
               ['U.S. History', 'SOCIAL'],
               ['U.S. Government', 'SOCIAL'],
               ['Economics', 'SOCIAL'],
               ['Physical Education', 'HEALTH'],
               ['Elective 1', 'ELECTIVE'],
               ['Elective 2', 'ELECTIVE'],
               ['Elective 3', 'ELECTIVE'],
               ['Elective 4', 'ELECTIVE'],
               ['Elective 5', 'ELECTIVE'],
               ['Elective 6', 'ELECTIVE'],
               ['Elective 7', 'ELECTIVE'],
               ['Elective 8', 'ELECTIVE'],
               ['ART 1', 'FINEART'],
               ['ART 2', 'FINEART'],
               ['ART 3', 'FINEART'],
               ['Study Hall', 'FREE']
               ]
    x = 0
    for c in courses:
        insert_course(x, c[0], c[1])
        x += 1


def insert_test_preferences():
    # Assume 1000 students with decreasing number count thru 9 to 12th greade

    # Note that Preference period is almost meaningless and is simply here for indexing in UI
    for x in range(0, 349):
        # ELA 9th grade everyone takes
        insert_preference(5, x, 1)

        # Math
        r = random.random()
        if (r < 0.9):
            insert_preference(0, x, 2)
        else:
            insert_preference(2, x, 2)

        # Science all 9th graders take bio
        insert_preference(9, x, 3)

        # Social
        r = random.random()
        if (r < 0.95):
            insert_preference(12, x, 4)
        else:
            insert_preference(13, x, 4)

        # Elective
        r = random.randint(17, 24)
        insert_preference(r, x, 5)

        # P.E
        insert_preference(16, x, 6)

        # Study Hall
        insert_preference(28, x, 7)

    for x in range(350, 649):
        # ELA 10th grade everyone takes around 2% fail and must retake
        r = random.random()
        if (r < 0.98):
            insert_preference(6, x, 1)
        else:
            insert_preference(5, x, 1)

        # Math
        r = random.random()
        if (r < 0.9):
            insert_preference(2, x, 2)
        elif (r < 0.98):
            insert_preference(1, x, 2)
        else:
            insert_preference(0, x, 2)

        # Science
        r = random.randint(10, 11)
        insert_preference(r, x, 3)

        # Social
        r = random.random()
        if r < 0.95:
            insert_preference(13, x, 4)
        else:
            insert_preference(14, x, 4)

        # Elective
        r = random.randint(17, 20)
        insert_preference(r, x, 5)

        r = random.randint(21, 27)
        insert_preference(r, x, 6)

        # Study Hall
        insert_preference(28, x, 7)

    for x in range(650, 900):
        # ELA 11th grade everyone takes around 2% fail and must retake
        r = random.random()
        if r < 0.98:
            insert_preference(7, x, 1)
        else:
            insert_preference(6, x, 1)

        # Math
        r = random.random()
        if r < 0.95:
            insert_preference(1, x, 2)
        else:
            r = random.randint(3, 4)
            insert_preference(r, x, 2)

        # Science
        r = random.randint(10, 11)
        insert_preference(r, x, 3)

        # Social
        r = random.random()
        if r < 0.95:
            insert_preference(14, x, 4)
        else:
            insert_preference(15, x, 4)

        # Elective
        r = random.randint(17, 20)
        insert_preference(r, x, 5)

        r = random.randint(21, 27)
        insert_preference(r, x, 6)

        # Study Hall
        insert_preference(28, x, 7)

    for x in range(900, 999):
        # ELA 12th grade everyone takes around 2% fail and must retake
        r = random.random()
        if r < 0.98:
            insert_preference(8, x, 1)
        else:
            insert_preference(7, x, 1)

        # Math
        r = random.randint(3, 4)
        insert_preference(r, x, 2)

        # Social
        r = random.random()
        if r < 0.98:
            insert_preference(15, x, 3)
        else:
            insert_preference(28, x, 3)

        # Study Hall
        insert_preference(28, x, 4)

        # Elective
        r = random.randint(17, 20)
        insert_preference(r, x, 5)

        r = random.randint(21, 27)
        insert_preference(r, x, 6)

        # Study Hall
        insert_preference(28, x, 7)


def insert_test_coursework():
    #student_id, name, credit, grade
    classes = ["Algebra 1", "Geometry", "ELA 1", "Biology 1", "World History", "Economics", "Elective 1", "ART 1", "Study Hall"]
    grade = ["A", "B", "C", "D"]
    for student in get_students():
        r1 = random.randint(0, 8)
        r2 = random.randint(0, 3)
        insert_class_history(student['id'], classes[r1], 3, grade[r2])
        r1 = random.randint(0, 8)
        r2 = random.randint(0, 3)
        insert_class_history(student['id'], classes[r1], 3, grade[r2])
        r1 = random.randint(0, 8)
        r2 = random.randint(0, 3)
        insert_class_history(student['id'], classes[r1], 3, grade[r2])