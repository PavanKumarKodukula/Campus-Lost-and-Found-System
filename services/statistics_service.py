import mysql.connector as SQLC

from connection import db_config


def get_statistics():

    try:
        cursor = db_config.cursor()

        # Total lost items
        cursor.execute("""
            SELECT COUNT(*)
            FROM lost_items
        """)
        total_lost = cursor.fetchone()[0]

        # Total found items
        cursor.execute("""
            SELECT COUNT(*)
            FROM found_items
        """)
        total_found = cursor.fetchone()[0]

        # Currently LOST
        cursor.execute("""
            SELECT COUNT(*)
            FROM lost_items
            WHERE status = 'LOST'
        """)
        currently_lost = cursor.fetchone()[0]

        # Currently FOUND
        cursor.execute("""
            SELECT COUNT(*)
            FROM lost_items
            WHERE status = 'FOUND'
        """)
        currently_found = cursor.fetchone()[0]

        # RETURNED items
        cursor.execute("""
            SELECT COUNT(*)
            FROM lost_items
            WHERE status = 'RETURNED'
        """)
        returned_items = cursor.fetchone()[0]

        cursor.close()

    except SQLC.Error as err:
        print("Database Error:", err)
        return None

    # Calculate return rate
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
