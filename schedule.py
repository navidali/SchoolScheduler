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

    # data structures need to be passed to rust

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
    # c_p_num = ctypes.c_int32

    c_c_id = create_string_buffer(4 * len(p_student_id))
    c_c_course_id = create_string_buffer(4 * len(p_student_id))
    c_c_period = create_string_buffer(4 * len(p_student_id))
    c_c_num = create_string_buffer(4)

    c_s_student_id = create_string_buffer(4 * len(p_student_id))
    c_s_class_id = create_string_buffer(4 * len(p_student_id))
    c_s_period = create_string_buffer(4 * len(p_student_id))
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
    print(int.from_bytes(c_c_id[0:4], byteorder='little'))

    p_c_c_num = int.from_bytes(c_c_num, byteorder='little')
    class_dict = dict()
    for x in range(p_c_c_num):
        Class.insert(int.from_bytes(c_c_id[(4 * x):((4 * x) + 4)], byteorder='little') - 1000,
                     int.from_bytes(c_c_course_id[(4 * x):((4 * x) + 4)], byteorder='little'),
                     int.from_bytes(c_c_period[(4 * x):((4 * x) + 4)], byteorder='little'))
        class_dict[x] = 0
    # TODO FIX HARD CODED STUDENT IDs

    for id in range(1000):

        pref = Preference.by_student_id(id)
        filled = []
        for p in pref:
            for x in range(1, 8):
                if x not in filled:
                    class_id_search = Class.by_course_id_period(p.course_id, x)
                    for c in class_id_search:
                        if class_dict[c] < 15 and Student.available(id, x):
                            Schedule.insert(id, c, x)
                            class_dict[c] = int(class_dict[c]) + 1
                            filled.append(x)
                            break
        # Check for empty slots in schedule
        for x in range(1, 8):
            if x not in filled:
                if Student.available(id, x):
                    Schedule.insert(id, -1, x)
    generate_pdfs()
    session.commit()

# Generate PDF schedules


def generate_pdfs():
    # pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    for x in range(1000):
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
            #print(sch)
            sch_class = ""
            if sch.class_id == -1:
                sch_class = "Study Hall"
            else:
                sch_class = Class.get_name(sch.class_id)
            # canvas.drawString(60, y_pos, f"Period {sch['period']}: {sch_class['name']}")
            data.append((f"Period {sch.period}", sch_class))
        table = Table(data, 2 * inch, .325 * inch)
        table.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 12), ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                                   ('LEFTPADDING', (1, 0), (-1, -1), 30),
                                   ('GRID', (0, 0), (-1, -1), 0.25, colors.black)]))
        table.wrapOn(canvas, 8 * inch, 8 * inch)
        table.drawOn(canvas, 60, 90)
        canvas.save()
