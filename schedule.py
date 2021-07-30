import ctypes
import math

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle

from ctypes import *

from db_alchemy import *


# assume that each class offering has the same id but can be multiple periods
def generate_schedule():
    # s = Schedule.by_student_id(0)

    #data structures need to be passed to rust

    #
    # Preferences course_id, student_id, period      Ready Only
    # Class       id, course_id, period              Read/Write     Output
    # Schedule    student_id, class_id, period       Read/Write     Output
    #

    lib = cdll.LoadLibrary('./sa.so')

    pref_al = Preference.get_all()

    p_course_id = []
    p_student_id = []
    p_period = []

    for pref in pref_al:
        p_course_id.append(pref.course_id)
        p_student_id.append(pref.student_id)
        p_period.append(pref.period)

    c_p_course_id = (ctypes.c_int32 * len(p_course_id))(*p_course_id)
    c_p_student_id = (ctypes.c_int32 * len(p_student_id))(*p_student_id)
    c_p_period = (ctypes.c_int32 * len(p_period))(*p_period)
    #c_p_num = ctypes.c_int32

    c_c_id = create_string_buffer(4*len(p_student_id))
    c_c_course_id = create_string_buffer(4*len(p_student_id))
    c_c_period = create_string_buffer(4*len(p_student_id))
    c_c_num = create_string_buffer(4)

    c_s_student_id = create_string_buffer(4*len(p_student_id))
    c_s_class_id = create_string_buffer(4*len(p_student_id))
    c_s_period = create_string_buffer(4*len(p_student_id))
    c_s_num = create_string_buffer(4)

    lib.schedule(c_p_course_id,
                 c_p_student_id,
                 c_p_period,
                 len(p_period),

                 c_c_id,
                 c_c_course_id,
                 c_c_period,
                 c_c_num,

                 c_s_student_id,
                 c_s_class_id,
                 c_s_period,
                 c_s_num)

    print(int.from_bytes(c_c_num, byteorder='little'))
    print(int.from_bytes(c_c_id[0:4],byteorder='little'))

    p_c_c_num = int.from_bytes(c_c_num, byteorder='little')

    for x in range(p_c_c_num):
        Class.insert(int.from_bytes(c_c_id[(4*x):((4*x)+4)],byteorder='little'), int.from_bytes(c_c_course_id[(4*x):((4*x)+4)]),int.from_bytes(c_c_period[(4*x):((4*x)+4)]))
        



"""


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



    pref = Preference.get_all()
    course_freq = {}
    for item in pref:
        if (item.course_id in course_freq):
            course_freq[item.course_id] += 1
        else:
            course_freq[item.course_id] = 1

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
            Class.insert(class_id, item, (x % 7) + 1)
            class_id += 1

    for id in range(10):

        pref = Preference.by_student_id(id)
        for p in pref:
            for x in range(1, 8):
                class_id_search = Course.available(p.course_id, x, id)
                if not class_id_search == -1 and Student.available(id, x):
                    Schedule.insert(id, class_id_search, x)
                    break
        # Check for empty slots in schedule
        for x in range(1, 8):
            if Student.available(id, x):
                Schedule.insert(Course.available(28, x, id), 28, x)

    generate_pdfs()

"""
# Generate PDF schedules


def generate_pdfs():
    #pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    for x in range(1):
        student = Student.by_id(x)
        schedules = Schedule.by_student_id(x)
        canvas = Canvas(f"export/{student.first}_{x}.pdf", pagesize=(8.5 * inch, 11 * inch / 2))
        y_pos = 330
        canvas.setFont('Helvetica', 16)
        canvas.drawString(60, y_pos, f"{student.first} {student.last}")
        canvas.setFont('Helvetica', 12)
        # fix grade to be in db?
        canvas.drawString(340, y_pos,
                          f"Student Id: {student.id}    GPA: {student.gpa}    Grade: {math.floor(student.id / 250 + 9)}")
        data = [("Class Period", "Class Name")]
        for sch in schedules:
            y_pos = y_pos - 36
            sch_class = Class.get_name(sch[0].class_id)
            # canvas.drawString(60, y_pos, f"Period {sch['period']}: {sch_class['name']}")
            data.append((f"Period {sch[0].period}", sch_class.name))
        table = Table(data, 2 * inch, .325 * inch)
        table.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 12), ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                                   ('LEFTPADDING', (1, 0), (-1, -1), 30),
                                   ('GRID', (0, 0), (-1, -1), 0.25, colors.black)]))
        table.wrapOn(canvas, 8 * inch, 8 * inch)
        table.drawOn(canvas, 60, 90)
        canvas.save()
