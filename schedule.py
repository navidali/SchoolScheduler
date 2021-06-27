import json
from db import *
from reportlab.pdfgen.canvas import Canvas

# assume that each class offering has the same id but can be multiple periods
def generate_schedule():
    #db.drop_schedules() # TODO: wipe schedule table
    idx = 1
    while idx <= 7:
        # get all schedules
        preferences = get_preferences_period(idx)
        for preference in preferences:
            # check if the course exists, and isn't full
            if course_available(preference['class_id'], preference['student_id'], preference['period']):  
                insert_schedule(preference['class_id'], preference['student_id'], idx)
            else:
                insert_schedule(0, preference['student_id'], idx)
        idx = idx + 1
    generate_pdfs()


# Generate PDF schedules
def generate_pdfs():
    students = get_students()
    for student in students:
        schedules = get_schedules_student(student['id'])
        canvas = Canvas(f"{student['id']}.pdf")    
        y_pos = 720
        canvas.drawString(72,y_pos, f"{student['first']} {student['last']}")
        canvas.drawString(396,y_pos, f"Student Id: {student['id']}")
        for sch in schedules:
            y_pos = y_pos - 36
            sch_class = get_classes_id_period(sch['class_id'], sch['period'])
            canvas.drawString(72, y_pos, f"Period {sch['period']}: {sch_class['name']}")
        canvas.save()
        
                
            
            
            
