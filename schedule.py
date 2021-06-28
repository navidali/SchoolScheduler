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

    class_id = 1000

    # insert_schedule()

    # Calcs min number of required courses to give all students a class
    for item in course_freq:
        num_classes = math.ceil(course_freq[item] / 15)

        # Creates an even distribution of classes for a given course over the 7 periods
        for x in range(1, num_classes + 1):
            insert_class(class_id, item, (x % 7) + 1)
            class_id += 1

    # generate_pdfs()

    # TODO FIX HARD CODED STUDENT IDs

    for id in range(100):

        pref = get_preference(id)
        for p in pref:
            for x in range(1, 8):
                class_id_search = course_available(p['course_id'], x, id)
                if not class_id_search == -1 and check_student_available(id, x):
                    insert_schedule(id, class_id_search, x)
                    break
        # Check for empty slots in schedule
        for x in range(1, 8):
            if check_student_available(id, x):
                insert_schedule(id, 28, x)

    generate_pdfs()


# Generate PDF schedules
def generate_pdfs():
    for x in range(100):
        student = get_student(x)
        schedules = get_schedules_student(x)
        canvas = Canvas(f"export/{student['first']}_{x}.pdf")
        y_pos = 720

        canvas.drawString(72, y_pos, f"{student['first']} {student['last']}")
        canvas.drawString(396, y_pos, f"Student Id: {student['id']}")
        for sch in schedules:
            y_pos = y_pos - 36
            sch_class = get_class_name(sch['class_id'])
            canvas.drawString(72, y_pos, f"Period {sch['period']}: {sch_class['name']}")
        canvas.save()
