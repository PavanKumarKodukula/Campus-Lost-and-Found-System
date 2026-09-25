import mysql.connector as SQLC

from connection import db_config

from models.found_item import FoundItem

from services.lost_item_service import (
    get_lost_items,
    update_lost_item_status,
    get_lost_item_by_id
)

from services.auth_service import get_user_by_id


def generate_found_id():

    query = """
        SELECT found_id
        FROM found_items
        ORDER BY found_id DESC
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
        return "F001"

    last_id = result[0]
    number = int(last_id[1:])

    return f"F{number + 1:03d}"


def find_lost_item(lost_id):

    return get_lost_item_by_id(lost_id)


def report_found_item(lost_id, finder_user_id, found_date, found_location):

    lost_item = find_lost_item(lost_id)

    if lost_item is None:
        return "Lost Item Not Found"

    if lost_item.get_status() != "LOST":
        return "This Item Is No Longer Available"

    found_id = generate_found_id()

    if found_id is None:
        return "Database Error: Could Not Generate Found ID"

    found_item = FoundItem(
        found_id,
        lost_id,
        finder_user_id,
        found_date,
        found_location,
        "FOUND"
    )

    query = """
        INSERT INTO found_items
        (found_id, lost_id, finder_user_id, found_date, found_location, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor = db_config.cursor()

        cursor.execute(
            query,
            (
                found_item.get_found_id(),
                found_item.get_lost_id(),
                found_item.get_finder_user_id(),
                found_item.get_found_date(),
                found_item.get_found_location(),
                found_item.get_status()
            )
        )

        db_config.commit()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return "Database Error: Could Not Report Found Item"

    update_lost_item_status(lost_id, "FOUND")

    return found_item


def get_found_items():

    query = """
        SELECT found_id, lost_id, finder_user_id,
               found_date, found_location, status
        FROM found_items
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return []

    found_items = []

    for row in rows:

        found_item = FoundItem(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        )

        found_items.append(found_item)

    return found_items


def display_found_items(found_items):

    if len(found_items) == 0:
        return False

    for item in found_items:

        print("\n" + "-" * 45)
        print("Found ID       :", item.get_found_id())
        print("Lost ID        :", item.get_lost_id())
        print("Finder User ID :", item.get_finder_user_id())
        print("Found Date     :", item.get_found_date())
        print("Found Location :", item.get_found_location())
        print("Status         :", item.get_status())
        print("-" * 45)

    return True


def get_my_found_items(user_id):

    query = """
        SELECT found_id, lost_id, finder_user_id,
               found_date, found_location, status
        FROM found_items
        WHERE finder_user_id = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return []

    found_items = []

    for row in rows:

        found_item = FoundItem(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        )

        found_items.append(found_item)

    return found_items


def get_found_item_by_id(found_id):

    query = """
        SELECT found_id, lost_id, finder_user_id,
               found_date, found_location, status
        FROM found_items
        WHERE found_id = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (found_id,))
        row = cursor.fetchone()
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    if row is None:
        return None

    found_item = FoundItem(
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5]
    )

    return found_item


def update_found_item_status(found_id, status):

    query = """
        UPDATE found_items
        SET status = %s
        WHERE found_id = %s
    """

    try:
        cursor = db_config.cursor()
        cursor.execute(query, (status, found_id))
        db_config.commit()
        updated = cursor.rowcount > 0
        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return False

    return updated


def claim_found_item(found_id, user_id):

    found_item = get_found_item_by_id(found_id)

    if found_item is None:
        return "Found Item Not Found"

    lost_item = get_lost_item_by_id(
        found_item.get_lost_id()
    )

    if lost_item is None:
        return "Lost Item Not Found"

    if lost_item.get_user_id() != user_id:
        return "Only the Owner Can Claim This Item"

    if found_item.get_status() != "FOUND":
        return "Item Is Already Returned"

    update_lost_item_status(
        found_item.get_lost_id(),
        "RETURNED"
    )

    update_found_item_status(
        found_id,
        "RETURNED"
    )

    return True


def get_contact_details(found_id, user_id):

    found_item = get_found_item_by_id(found_id)

    if found_item is None:
        return None

    lost_item = get_lost_item_by_id(
        found_item.get_lost_id()
    )

    if lost_item is None:
        return None

    owner_id = lost_item.get_user_id()
    finder_id = found_item.get_finder_user_id()

    if user_id == owner_id:

        contact_user = get_user_by_id(finder_id)

        return {
            "role": "owner",
            "contact": contact_user
        }

    if user_id == finder_id:

        contact_user = get_user_by_id(owner_id)

        return {
            "role": "finder",
            "contact": contact_user
        }

    return {
        "role": "other",
        "contact": None
    }
