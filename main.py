from db import *
from schedule import *

def insert_test_students():
    #(id, first, last, GPA)
    insert_student(1, "Joe", "Perez", 4.2)
    insert_student(2, "Alan", "Lee", 3.75)
    insert_student(3, "Ryan", "Gonzalez", 3.9)
    #get_students()
    
def insert_test_classes():
    #(id, name, period, capacity(optional))
    insert_class(1, "Algebra 1", 1)
    insert_class(2, "Biology 1", 2)
    insert_class(3, "Physcial Education", 3)
    insert_class(4, "ELA 1", 4)
    insert_class(1, "Algebra 1", 2)
    insert_class(5, "Algebra 2", 5)
    insert_class(6, "World History",6)
    insert_class(7, "U.S. History", 7)
    insert_class(8, "Economics", 1)
    insert_class(9, "U.S. Government", 3)
    #get_classes()
    
def insert_test_preferences():
    #(class_id, student_id, period)
    insert_preference(1, 1, 1)
    insert_preference(2, 1, 2)
    insert_preference(3, 1, 3)
    insert_preference(4, 1, 4)
    insert_preference(5, 1, 5)
    insert_preference(6, 1, 6)
    insert_preference(7, 1, 7)
    insert_preference(8, 2, 1)
    insert_preference(2, 2, 2)
    insert_preference(9, 2, 3)
    insert_preference(4, 2, 4)
    insert_preference(5, 2, 5)
    insert_preference(6, 2, 6)
    insert_preference(7, 2, 7)
    
def main():
    insert_test_students()
    insert_test_classes()
    insert_test_preferences()
    generate_schedule()
    get_schedules()


if __name__ == '__main__':
    delete_all()
    db_init()
    main()
    db_close()
