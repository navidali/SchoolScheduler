import math

from reportlab.pdfgen.canvas import Canvas

from db import *


# assume that each class offering has the same id but can be multiple periods
def generate_schedule():
    # db.drop_schedules() # TODO: wipe schedule table

    # idx = 1
    # while idx <= 7:
    #    # get all schedules
    #    preferences = get_preferences_period(idx)
    #    for preference in preferences:
    #        # check if the course exists, and isn't full
    #        if course_available(preference['class_id'], preference['student_id'], preference['period']):
    #            insert_schedule(preference['class_id'], preference['student_id'], idx)
    #        else:
    #            insert_schedule(0, preference['student_id'], idx)
    #    idx = idx + 1

    # Computer Min Required Class to reduce searchable zone for valid schedules

    pref = get_preferences()
    course_freq = {}
    for item in pref:
        if (item['course_id'] in course_freq):
            course_freq[item['course_id']] += 1
        else:
            course_freq[item['course_id']] = 1

    print(course_freq)

    # For now assume all classes have a 15 student cap thus for a best case even distrubtion number of request
    # classes is /15 and rounded up Simple Greedy Algorithm is used for now until offical algorithm can be
    # implamented in C/Rust Also note this method ignores that fact that not all teachers can be everything breaking
    # down the model

    for item in course_freq:
        print(item)
        print(course_freq[item])
        num_classes = math.ceil(course_freq[item] / 15)
        print(num_classes)
        print('')

        for x in range(1, num_classes):
            print(x)

    # generate_pdfs()


# Generate PDF schedules
def generate_pdfs():
    students = get_students()
    for student in students:
        schedules = get_schedules_student(student['id'])
        canvas = Canvas(f"{student['id']}.pdf")
        y_pos = 720
        canvas.drawString(72, y_pos, f"{student['first']} {student['last']}")
        canvas.drawString(396, y_pos, f"Student Id: {student['id']}")
        for sch in schedules:
            y_pos = y_pos - 36
            sch_class = get_classes_id_period(sch['class_id'], sch['period'])
            canvas.drawString(72, y_pos, f"Period {sch['period']}: {sch_class['name']}")
        canvas.save()
