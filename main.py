from db import *


def main():
    insert_student(1, "Joe", "Perez", 4.2)
    insert_student(2, "Alan", "Lee", 3.75)
    insert_student(3, "Ryan", "Gonzalez", 3.9)
    get_students()
    insert_class(1, "Algebra 1")
    insert_class(1, "Biology 1")
    insert_class(1, "Physcial Education")
    insert_class(2, "ELA 1")
    insert_class(2, "Algebra 1")
    insert_class(2, "Algebra 2")
    insert_class(3, "World History")
    insert_class(3, "U.S. History")
    insert_class(3, "Economics")
    insert_class(3, "U.S. Government")
    get_classes()


if __name__ == '__main__':
    delete_all()
    db_init()
    main()
    db_close()
