import xlsxwriter
import random

def write_tuple(worksheet, data, row):
    col = 0
    for d in data:
        worksheet.write(row, col, d)
        col += 1


def generate_test_data():
    workbook = xlsxwriter.Workbook('import/Data.xlsx')
    insert_test_students(workbook)
    insert_test_courses(workbook)
    insert_test_preferences(workbook)
    workbook.close()


def insert_test_students(workbook):
    worksheet_students = workbook.add_worksheet("Students")
    worksheet_coursework = workbook.add_worksheet("Coursework")
    # (id, first, last, GPA)
    words = open('words.txt', 'r')
    lines = words.read().splitlines()

    coursework_row = 0

    for x in range(1000):
        grade = 9
        if x in range(350,650): grade = 10
        elif x in range(650,900): grade = 11
        elif x in range(900,1000): grade = 12
        write_tuple(worksheet_students, (x, lines[random.randint(0, 10000)], lines[random.randint(0, 10000)], grade), x)
        coursework_row = insert_test_coursework(worksheet_coursework, (x, lines[random.randint(0, 10000)], lines[random.randint(0, 10000)]), coursework_row)


def insert_test_courses(workbook):
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
    worksheet = workbook.add_worksheet("Courses")
    x = 0
    for c in courses:
        write_tuple(worksheet, (x, c[0], c[1], 15), x)
        x += 1


def insert_test_preferences(workbook):
    # Assume 1000 students with decreasing number count thru 9 to 12th greade
    # Note that Preference period is almost meaningless and is simply here for indexing in UI
    worksheet = workbook.add_worksheet("Preferences")
    row = 0
    for x in range(0, 349):
        # ELA 9th grade everyone takes
        write_tuple(worksheet, (5, x, 1), row)
        row += 1

        # Math
        r = random.random()
        if (r < 0.9):
            write_tuple(worksheet, (0, x, 2), row)
        else:
            write_tuple(worksheet, (2, x, 2), row)
        row += 1

        # Science all 9th graders take bio
        write_tuple(worksheet, (9, x, 3), row)
        row += 1

        # Social
        r = random.random()
        if (r < 0.95):
            write_tuple(worksheet, (12, x, 4), row)
        else:
            write_tuple(worksheet, (13, x, 4), row)
        row += 1

        # Elective
        r = random.randint(17, 24)
        write_tuple(worksheet, (r, x, 5), row)
        row += 1

        # P.E
        write_tuple(worksheet, (16, x, 6), row)
        row += 1

        # Study Hall
        write_tuple(worksheet, (28, x, 7), row)
        row += 1

    for x in range(350, 649):
        # ELA 10th grade everyone takes around 2% fail and must retake
        r = random.random()
        if (r < 0.98):
            write_tuple(worksheet, (6, x, 1), row)
        else:
            write_tuple(worksheet, (5, x, 1), row)
        row += 1

        # Math
        r = random.random()
        if (r < 0.9):
            write_tuple(worksheet, (2, x, 2), row)
        elif (r < 0.98):
            write_tuple(worksheet, (1, x, 2), row)
        else:
            write_tuple(worksheet, (0, x, 2), row)
        row += 1

        # Science
        r = random.randint(10, 11)
        write_tuple(worksheet, (r, x, 3), row)
        row += 1

        # Social
        r = random.random()
        if r < 0.95:
            write_tuple(worksheet, (13, x, 4), row)
        else:
            write_tuple(worksheet, (14, x, 4), row)
        row += 1

        # Elective
        r = random.randint(17, 20)
        write_tuple(worksheet, (r, x, 5), row)
        row += 1

        r = random.randint(21, 27)
        write_tuple(worksheet, (r, x, 6), row)
        row += 1

        # Study Hall
        write_tuple(worksheet, (28, x, 7), row)
        row += 1

    for x in range(650, 900):
        # ELA 11th grade everyone takes around 2% fail and must retake
        r = random.random()
        if r < 0.98:
            write_tuple(worksheet, (7, x, 1), row)
        else:
            write_tuple(worksheet, (6, x, 1), row)
        row += 1

        # Math
        r = random.random()
        if r < 0.95:
            write_tuple(worksheet, (1, x, 2), row)
        else:
            r = random.randint(3, 4)
            write_tuple(worksheet, (r, x, 2), row)
        row += 1

        # Science
        r = random.randint(10, 11)
        write_tuple(worksheet, (r, x, 3), row)
        row += 1

        # Social
        r = random.random()
        if r < 0.95:
            write_tuple(worksheet, (14, x, 4), row)
        else:
            write_tuple(worksheet, (15, x, 4), row)
        row += 1

        # Elective
        r = random.randint(17, 20)
        write_tuple(worksheet, (r, x, 5), row)
        row += 1

        r = random.randint(21, 27)
        write_tuple(worksheet, (r, x, 6), row)
        row += 1

        # Study Hall
        write_tuple(worksheet, (28, x, 7), row)
        row += 1

    for x in range(900, 1000):
        # ELA 12th grade everyone takes around 2% fail and must retake
        r = random.random()
        if r < 0.98:
            write_tuple(worksheet, (8, x, 1), row)
        else:
            write_tuple(worksheet, (7, x, 1), row)
        row += 1

        # Math
        r = random.randint(3, 4)
        write_tuple(worksheet, (r, x, 2), row)
        row += 1

        # Social
        r = random.random()
        if r < 0.98:
            write_tuple(worksheet, (15, x, 3), row)
        else:
            write_tuple(worksheet, (28, x, 3), row)
        row += 1

        # Study Hall
        write_tuple(worksheet, (28, x, 4), row)
        row += 1

        # Elective
        r = random.randint(17, 20)
        write_tuple(worksheet, (r, x, 5), row)
        row += 1

        r = random.randint(21, 27)
        write_tuple(worksheet, (r, x, 6), row)
        row += 1

        # Study Hall
        write_tuple(worksheet, (28, x, 7), row)
        row += 1

# def insert_test_coursework(worksheet, student, row):
#     #student_id, name, credit, grade
#     classes = ["Algebra 1", "Geometry", "ELA 1", "Biology 1", "World History", "Economics", "Elective 1", "ART 1", "Study Hall"]
#     grade = ["A", "B", "C", "D"]
#
#     r1 = random.randint(0, 8)
#     r2 = random.randint(0, 3)
#     write_tuple(worksheet, (student[0], classes[r1], 3, grade[r2]), row)


def insert_test_coursework(worksheet, student, row):
    # student_id, name, credit, grade
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
    x = student[0]
    failed = []
    classes = []
    if x in range(350,1000):
        write_tuple(worksheet, (x, courses[5][0], 3, get_grade(failed, courses[5][0])), row)
        classes.append(courses[5][0])
        row += 1

        r = random.random()
        if (r < 0.9):
            write_tuple(worksheet, (x, courses[0][0], 3, get_grade(failed, courses[0][0])), row)
            classes.append(courses[0][0])
            row += 1
        else:
            write_tuple(worksheet, (x, courses[2][0], 3, get_grade(failed, courses[2][0])), row)
            classes.append(courses[2][0])
            row += 1

        write_tuple(worksheet, (x, courses[9][0], 3, get_grade(failed, courses[9][0])), row)
        classes.append(courses[9][0])
        row += 1

        r = random.random()
        if (r < 0.95):
            write_tuple(worksheet, (x, courses[12][0], 3, get_grade(failed, courses[12][0])), row)
            classes.append(courses[12][0])
            row += 1
        else:
            write_tuple(worksheet, (x, courses[13][0], 3, get_grade(failed, courses[13][0])), row)
            classes.append(courses[13][0])
            row += 1

        r = random.randint(17, 24)
        write_tuple(worksheet, (x, courses[r][0], 1, get_grade(failed, courses[r][0])), row)
        classes.append(courses[r][0])
        row += 1

        write_tuple(worksheet, (x, courses[16][0], 3, get_grade(failed, courses[16][0])), row)
        classes.append(courses[16][0])
        row += 1

        write_tuple(worksheet, (x, courses[28][0], 1, get_grade(failed, courses[28][0])), row)
        classes.append(courses[28][0])
        row += 1

        if x in range(650, 1000):
            #failed = classes_failed(x)
            #classes = Class_History.by_student_id(x)

            if "ELA 1" in failed:
                write_tuple(worksheet, (x, courses[5][0], 3, get_grade(failed, courses[5][0])), row)
                classes.append(courses[5][0])
                row += 1
            else:
                write_tuple(worksheet, (x, courses[6][0], 3, get_grade(failed, courses[6][0])), row)
                classes.append(courses[6][0])
                row += 1

            # Math
            r = random.random()
            if "Algebra 1" in failed:
                write_tuple(worksheet, (x, courses[0][0], 3, get_grade(failed, courses[0][0])), row)
                classes.append(courses[0][0])
                row += 1
            elif "Geometry" in failed:
                write_tuple(worksheet, (x, courses[2][0], 3, get_grade(failed, courses[2][0])), row)
                classes.append(courses[2][0])
                row += 1
            else:
                if [y for y in classes if y == "Algebra 1"]:
                    if r < 0.9:
                        write_tuple(worksheet, (x, courses[2][0], 3, get_grade(failed, courses[2][0])), row)
                        classes.append(courses[2][0])
                        row += 1
                    else:
                        write_tuple(worksheet, (x, courses[1][0], 3, get_grade(failed, courses[1][0])), row)
                        classes.append(courses[1][0])
                        row += 1
                elif [y for y in classes if y == "Geometry"]:
                    write_tuple(worksheet, (x, courses[0][0], 3, get_grade(failed, courses[0][0])), row)
                    classes.append(courses[0][0])
                    row += 1

            # Science
            if "Biology 1" in failed:
                write_tuple(worksheet, (x, courses[9][0], 3, get_grade(failed, courses[9][0])), row)
                classes.append(courses[9][0])
                row += 1
            else:
                r = random.randint(10, 11)
                write_tuple(worksheet, (x, courses[r][0], 3, get_grade(failed, courses[r][0])), row)
                classes.append(courses[r][0])
                row += 1

            # Social
            if "World History" in failed:
                write_tuple(worksheet, (x, courses[12][0], 3, get_grade(failed, courses[12][0])), row)
                classes.append(courses[12][0])
                row += 1
            elif "U.S. History" in failed:
                write_tuple(worksheet, (x, courses[13][0], 3, get_grade(failed, courses[13][0])), row)
                classes.append(courses[13][0])
                row += 1
            else:
                if [y for y in classes if y == "World History"]:
                    r = random.random()
                    if r < 0.95:
                        write_tuple(worksheet, (x, courses[13][0], 3, get_grade(failed, courses[13][0])), row)
                        classes.append(courses[13][0])
                        row += 1
                    else:
                        write_tuple(worksheet, (x, courses[14][0], 3, get_grade(failed, courses[14][0])), row)
                        classes.append(courses[14][0])
                        row += 1
                else:
                    write_tuple(worksheet, (x, courses[14][0], 3, get_grade(failed, courses[14][0])), row)
                    classes.append(courses[14][0])
                    row += 1

            # Elective
            r = random.randint(17, 20)
            write_tuple(worksheet, (x, courses[r][0], 3, get_grade(failed, courses[r][0])), row)
            classes.append(courses[r][0])
            row += 1

            r = random.randint(21, 27)
            write_tuple(worksheet, (x, courses[r][0], 3, get_grade(failed, courses[r][0])), row)
            classes.append(courses[r][0])
            row += 1

            # Study Hall
            write_tuple(worksheet, (x, courses[28][0], 3, get_grade(failed, courses[28][0])), row)
            classes.append(courses[28][0])
            row += 1

        if x in range(900, 1000):
            #failed = classes_failed(x)
            #classes = Class_History.by_student_id(x)

            if "ELA 2" in failed:
                write_tuple(worksheet, (x, courses[6][0], 3, get_grade(failed, courses[6][0])), row)
                classes.append(courses[6][0])
                row += 1
            else:
                write_tuple(worksheet, (x, courses[7][0], 3, get_grade(failed, courses[7][0])), row)
                classes.append(courses[7][0])
                row += 1

            # Math
            if "Algebra 2" in failed or [y for y in classes if y != "Algebra 2"] and [y for y in classes if y == "Algebra 1"]:
                write_tuple(worksheet, (x, courses[1][0], 3, get_grade(failed, courses[1][0])), row)
                classes.append(courses[1][0])
                row += 1
            elif [y for y in classes if y == "Algebra 1"]:
                write_tuple(worksheet, (x, courses[0][0], 3, get_grade(failed, courses[0][0])), row)
                classes.append(courses[0][0])
                row += 1
            else:
                r = random.randint(3, 4)
                write_tuple(worksheet, (x, courses[r][0], 3, get_grade(failed, courses[r][0])), row)
                classes.append(courses[r][0])
                row += 1

            # Science
            if "Biology 1" in failed:
                write_tuple(worksheet, (x, courses[9][0], 3, get_grade(failed, courses[9][0])), row)
                classes.append(courses[9][0])
                row += 1
            elif "Science Class 1" in failed:
                write_tuple(worksheet, (x, courses[10][0], 3, get_grade(failed, courses[10][0])), row)
                classes.append(courses[10][0])
                row += 1
            elif "Science Class 2" in failed:
                write_tuple(worksheet, (x, courses[11][0], 3, get_grade(failed, courses[11][0])), row)
                classes.append(courses[11][0])
                row += 1
            else:
                if [y for y in classes if y == "Science Class 1"]:
                    write_tuple(worksheet, (x, courses[11][0], 3, get_grade(failed, courses[11][0])), row)
                    classes.append(courses[11][0])
                    row += 1
                else:
                    write_tuple(worksheet, (x, courses[10][0], 3, get_grade(failed, courses[10][0])), row)
                    classes.append(courses[10][0])
                    row += 1

            # Social
            if "U.S. History" in failed:
                write_tuple(worksheet, (x, courses[13][0], 3, get_grade(failed, courses[13][0])), row)
                classes.append(courses[13][0])
                row += 1
            elif "U.S. Government" in failed:
                write_tuple(worksheet, (x, courses[14][0], 3, get_grade(failed, courses[14][0])), row)
                classes.append(courses[14][0])
                row += 1
            else:
                if [y for y in classes if y == "U.S. Government"]:
                    write_tuple(worksheet, (x, courses[15][0], 3, get_grade(failed, courses[15][0])), row)
                    classes.append(courses[15][0])
                    row += 1
                else:
                    write_tuple(worksheet, (x, courses[14][0], 3, get_grade(failed, courses[14][0])), row)
                    classes.append(courses[14][0])
                    row += 1

            # Elective
            r = random.randint(17, 20)
            write_tuple(worksheet, (x, courses[r][0], 3, get_grade(failed, courses[r][0])), row)
            classes.append(courses[r][0])
            row += 1

            r = random.randint(21, 27)
            write_tuple(worksheet, (x, courses[r][0], 3, get_grade(failed, courses[r][0])), row)
            classes.append(courses[r][0])
            row += 1

            # Study Hall
            write_tuple(worksheet, (x, courses[28][0], 3, get_grade(failed, courses[28][0])), row)
            classes.append(courses[28][0])
            row += 1
    return row


def get_grade(failed, class_name):
    r = random.random()
    if r <= 0.6:
        return "A"
    elif r <= 0.8:
        return "B"
    elif r <= 0.925:
        return "C"
    elif r <= .98:
        return "D"
    else:
        failed.append(class_name)
        return "F"


# def classes_failed(student_id):
#     failed = []
#     for c in Class_History.by_student_id(student_id)[:-7]:
#         if c.grade == "F":
#             failed.append(c.class_name)
#     return failed
