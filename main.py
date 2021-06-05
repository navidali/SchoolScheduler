from db import *


def main():
    insert_student("test", 10)
    get_students()


if __name__ == '__main__':
    db_init()
    main()
    db_close()
