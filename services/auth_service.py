import mysql.connector as SQLC

from connection import db_config

from models.student import Student
from models.admin import Admin


def generate_student_id():

    query = """
        SELECT user_id
        FROM users
        WHERE role = 'student'
        ORDER BY user_id DESC
        LIMIT 1
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    if result is None:
        return "S101"

    last_id = result[0]
    number = int(last_id[1:])

    return f"S{number + 1:03d}"


def check_duplicate_student(college_id, email):

    query = """
        SELECT college_id, email
        FROM users
        WHERE college_id = %s OR email = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (college_id, email))
        result = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return "Database Error: Could Not Check Duplicate"

    if result is None:
        return None

    if result[0] == college_id:
        return "College ID already registered"

    if result[1] == email:
        return "Email already registered"

    return None


def register_student(name, college_id, email, phone, password):

    duplicate = check_duplicate_student(college_id, email)

    if duplicate is not None:
        return duplicate

    user_id = generate_student_id()

    if user_id is None:
        return "Database Error: Could Not Generate Student ID"

    student = Student(
        user_id,
        name,
        college_id,
        email,
        phone,
        password
    )

    query = """
        INSERT INTO users
        (user_id, name, college_id, email, phone, password, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor = db_config.cursor()

        cursor.execute(
            query,
            (
                student.get_user_id(),
                student.get_name(),
                student.get_college_id(),
                student.get_email(),
                student.get_phone(),
                student.get_password(),
                student.get_role()
            )
        )

        db_config.commit()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return "Database Error: Could Not Register Student"

    return student


def login(email, password):

    query = """
        SELECT user_id, name, college_id, email, phone, password, role
        FROM users
        WHERE email = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    if user is None:
        return None

    # check password ourselves so it is compared exactly, case-sensitively
    if user[5] != password:
        return None

    user_id = user[0]
    name = user[1]
    college_id = user[2]
    email = user[3]
    phone = user[4]
    password = user[5]
    role = user[6]

    if role == "student":
        return Student(
            user_id,
            name,
            college_id,
            email,
            phone,
            password
        )

    elif role == "admin":
        return Admin(
            user_id,
            name,
            college_id,
            email,
            phone,
            password
        )

    return None


def get_user_by_id(user_id):

    query = """
        SELECT user_id, name, email, phone
        FROM users
        WHERE user_id = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    if user is None:
        return None

    return {
        "user_id": user[0],
        "name": user[1],
        "email": user[2],
        "phone": user[3]
    }


def get_all_students():

    query = """
        SELECT user_id, name, college_id, email, phone
        FROM users
        WHERE role = 'student'
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return []

    return students
