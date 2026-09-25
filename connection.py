import mysql.connector as SQLC
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

try:
    # step 1: connect to mysql server first (without selecting a database)
    temp_conn = SQLC.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        use_pure=True
    )

    temp_cursor = temp_conn.cursor()

    # create the database if it is not already there
    temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

    temp_cursor.close()
    temp_conn.close()

    # step 2: now connect to our actual database
    db_config = SQLC.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        use_pure=True,
        database=DB_NAME
    )

    print("Database connected successfully!")

    cursor = db_config.cursor()

    # step 3: create tables if they are not already there

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100),
            college_id VARCHAR(50) UNIQUE,
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(20),
            password VARCHAR(100),
            role VARCHAR(20)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lost_items (
            lost_id VARCHAR(10) PRIMARY KEY,
            user_id VARCHAR(10),
            item_name VARCHAR(100),
            category VARCHAR(50),
            description TEXT,
            location VARCHAR(100),
            date VARCHAR(20),
            status VARCHAR(20)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS found_items (
            found_id VARCHAR(10) PRIMARY KEY,
            lost_id VARCHAR(10),
            finder_user_id VARCHAR(10),
            found_date VARCHAR(20),
            found_location VARCHAR(100),
            status VARCHAR(20)
        )
    """)

    db_config.commit()

    # step 4: insert the default admin row only if it is not already there

    cursor.execute("SELECT * FROM users WHERE user_id = 'A001'")
    admin_row = cursor.fetchone()

    if admin_row is None:

        cursor.execute(
            """
            INSERT INTO users
            (user_id, name, college_id, email, phone, password, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            ("A001", "Admin", "ADMIN001", "admin@campus.com", "9999999999", "admin@123", "admin")
        )

        db_config.commit()
        print("Default admin account created.")

    cursor.close()

except SQLC.Error as err:
    print("Database Connection Failed:", err)
    db_config = None