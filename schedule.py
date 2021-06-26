import json
from db import *

# assume that each class offering has the same id but can be multiple periods
def generate_schedule():
    #db.drop_schedules() # wipe schedule table
    idx = 1
    while idx <= 7:
        # get all schedules
        preferences = get_preferences_period(idx)
        for p in preferences:
            preference = dict(p)
            # check if the course exists, and isn't full
            if course_available(preference['class_id'], preference['student_id'], preference['period']):  
                insert_schedule(preference['class_id'], preference['student_id'], idx)
            else:
                insert_schedule(0, preference['student_id'], idx)
        idx = idx + 1
                    
                
            
            
            
