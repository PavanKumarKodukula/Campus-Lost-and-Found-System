import mysql.connector as SQLC

from connection import db_config
from models.lost_item import LostItem


def generate_lost_id():

    query = """
        SELECT lost_id
        FROM lost_items
        ORDER BY lost_id DESC
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
        return "L001"

    last_id = result[0]
    number = int(last_id[1:])

    return f"L{number + 1:03d}"


def report_lost_item(user_id, item_name, category, description, location, date):

    lost_id = generate_lost_id()

    if lost_id is None:
        return "Database Error: Could Not Generate Lost ID"

    lost_item = LostItem(
        lost_id,
        user_id,
        item_name,
        category,
        description,
        location,
        date,
        "LOST"
    )

    query = """
        INSERT INTO lost_items
        (lost_id, user_id, item_name, category, description, location, date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor = db_config.cursor()

        cursor.execute(
            query,
            (
                lost_item.get_lost_id(),
                lost_item.get_user_id(),
                lost_item.get_item_name(),
                lost_item.get_category(),
                lost_item.get_description(),
                lost_item.get_location(),
                lost_item.get_date(),
                lost_item.get_status()
            )
        )

        db_config.commit()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return "Database Error: Could Not Report Lost Item"

    return lost_item


def get_lost_items():

    query = """
        SELECT lost_id, user_id, item_name, category,
               description, location, date, status
        FROM lost_items
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return []

    lost_items = []

    for row in rows:

        lost_item = LostItem(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7]
        )

        lost_items.append(lost_item)

    return lost_items


def update_lost_item_status(lost_id, status):

    query = """
        UPDATE lost_items
        SET status = %s
        WHERE lost_id = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (status, lost_id))
        db_config.commit()
        updated = cursor.rowcount > 0
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return False

    return updated


def display_lost_items(lost_items):

    if len(lost_items) == 0:
        return False

    for item in lost_items:

        print("\n" + "-" * 45)
        print("Lost ID     :", item.get_lost_id())
        print("Item Name   :", item.get_item_name())
        print("Category    :", item.get_category())
        print("Description :", item.get_description())
        print("Location    :", item.get_location())
        print("Date        :", item.get_date())
        print("Status      :", item.get_status())
        print("-" * 45)

    return True


def get_my_lost_items(user_id):

    query = """
        SELECT lost_id, user_id, item_name, category,
               description, location, date, status
        FROM lost_items
        WHERE user_id = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return []

    lost_items = []

    for row in rows:

        lost_item = LostItem(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7]
        )

        lost_items.append(lost_item)

    return lost_items


def get_lost_item_by_id(lost_id):

    query = """
        SELECT lost_id, user_id, item_name, category,
               description, location, date, status
        FROM lost_items
        WHERE lost_id = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (lost_id,))
        row = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    if row is None:
        return None

    lost_item = LostItem(
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[7]
    )

    return lost_item
