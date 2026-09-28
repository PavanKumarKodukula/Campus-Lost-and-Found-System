import mysql.connector as SQLC

from connection import db_config


def get_statistics():

    try:
        cursor = db_config.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM lost_items")
        total_lost = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM found_items")
        total_found = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM lost_items WHERE status = 'LOST'")
        currently_lost = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM lost_items WHERE status = 'FOUND'")
        currently_found = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM lost_items WHERE status = 'RETURNED'")
        returned_items = cursor.fetchone()["total"]

        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    return_rate = 0

    if total_found > 0:
        return_rate = (returned_items / total_found) * 100

    return {
        "total_lost": total_lost,
        "total_found": total_found,
        "currently_lost": currently_lost,
        "currently_found": currently_found,
        "returned_items": returned_items,
        "return_rate": return_rate
    }
