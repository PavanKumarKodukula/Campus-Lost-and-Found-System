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
        cursor = db_config.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    if result is None:
        return "S101"

    number = int(result["user_id"][1:])

    return f"S{number + 1:03d}"


def check_duplicate_student(college_id, email):

    query = """
        SELECT college_id, email
        FROM users
        WHERE college_id = %s OR email = %s
    """

    try:
        cursor = db_config.cursor(dictionary=True)
        cursor.execute(query, (college_id, email))
        result = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return "Database Error: Could Not Check Duplicate"

    if result is None:
        return None

    if result["college_id"] == college_id:
        return "College ID already registered"

    if result["email"] == email:
        return "Email already registered"

    return None


def register_student(name, college_id, email, phone, password):

    if name.strip() == "":
        return "Name cannot be empty"

    if college_id.strip() == "":
        return "College ID cannot be empty"

    if email.strip() == "":
        return "Email cannot be empty"

    if phone.strip() == "":
        return "Phone number cannot be empty"

    if password.strip() == "":
        return "Password cannot be empty"

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
        cursor = db_config.cursor(dictionary=True)
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    if user is None or user["password"] != password:
        return None

    details = (
        user["user_id"],
        user["name"],
        user["college_id"],
        user["email"],
        user["phone"],
        user["password"]
    )

    if user["role"] == "student":
        return Student(*details)

    if user["role"] == "admin":
        return Admin(*details)

    return None


def get_user_by_id(user_id):

    query = """
        SELECT user_id, name, email, phone
        FROM users
        WHERE user_id = %s
    """

    try:
        cursor = db_config.cursor(dictionary=True)
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    return user


def get_all_students():

    query = """
        SELECT user_id, name, college_id, email, phone
        FROM users
        WHERE role = 'student'
    """

    try:
        cursor = db_config.cursor(dictionary=True)
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return []

    return students
