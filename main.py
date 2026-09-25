from datetime import datetime

from services.auth_service import register_student, login, get_all_students

from services.lost_item_service import (
    report_lost_item,
    get_lost_items,
    display_lost_items,
    get_my_lost_items
)

from services.found_item_service import (
    report_found_item,
    get_found_items,
    display_found_items,
    get_my_found_items,
    get_contact_details,
    claim_found_item
)

from services.statistics_service import get_statistics


def student_menu(user):

    while True:

        print("\n" + "=" * 45)
        print("          STUDENT DASHBOARD")
        print("=" * 45)
        print("1. Report Lost Item")
        print("2. Report Found Item")
        print("3. View Lost Items")
        print("4. View Found Items")
        print("5. My Reports")
        print("6. Logout")
        print("7. Contact Found Item")
        print("8. Claim Found Item")
        print("=" * 45)

        choice = input("Enter Your Choice: ")

        # --------------------------------------------------
        # 1. REPORT LOST ITEM
        # --------------------------------------------------

        if choice == "1":

            item_name = input("Enter Item Name: ")
            category = input("Enter Category: ")
            description = input("Enter Description: ")
            location = input("Enter Lost Location: ")
            date = input("Enter Lost Date (YYYY-MM-DD): ")

            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue

            lost_item = report_lost_item(
                user.get_user_id(),
                item_name,
                category,
                description,
                location,
                date
            )

            if isinstance(lost_item, str):

                print(lost_item)

            else:

                print("\nLost Item Reported Successfully")
                print("Lost ID:", lost_item.get_lost_id())

        # --------------------------------------------------
        # 2. REPORT FOUND ITEM
        # --------------------------------------------------

        elif choice == "2":

            lost_items = get_lost_items()
            available_items = []

            for item in lost_items:

                if item.get_status() == "LOST":
                    available_items.append(item)

            if len(available_items) == 0:

                print("No Lost Items Available To Report As Found")

            else:

                print("\n" + "=" * 45)
                print("       AVAILABLE LOST ITEMS")
                print("=" * 45)

                for item in available_items:

                    print(
                        f"{item.get_lost_id()} | "
                        f"{item.get_item_name()} | "
                        f"{item.get_category()} | "
                        f"{item.get_location()}"
                    )

                lost_id = input("\nEnter Lost ID: ")
                found_date = input("Enter Found Date (YYYY-MM-DD): ")

                try:
                    datetime.strptime(found_date, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
                    continue

                found_location = input("Enter Found Location: ")

                result = report_found_item(
                    lost_id,
                    user.get_user_id(),
                    found_date,
                    found_location
                )

                if isinstance(result, str):

                    print(result)

                else:

                    print("\nFound Item Reported Successfully")
                    print("Found ID:", result.get_found_id())
                    print("Lost ID:", result.get_lost_id())

        # --------------------------------------------------
        # 3. VIEW LOST ITEMS
        # --------------------------------------------------

        elif choice == "3":

            lost_items = get_lost_items()

            if not display_lost_items(lost_items):

                print("No Lost Items Available")

        # --------------------------------------------------
        # 4. VIEW FOUND ITEMS
        # --------------------------------------------------

        elif choice == "4":

            found_items = get_found_items()

            if not display_found_items(found_items):

                print("No Found Items Available")

        # --------------------------------------------------
        # 5. MY REPORTS
        # --------------------------------------------------

        elif choice == "5":

            print("\n" + "=" * 45)
            print("             MY LOST REPORTS")
            print("=" * 45)

            my_lost_items = get_my_lost_items(
                user.get_user_id()
            )

            if not my_lost_items:

                print("No Lost Reports")

            else:

                for item in my_lost_items:

                    print("\n" + "-" * 45)
                    print("Lost ID     :", item.get_lost_id())
                    print("Item Name   :", item.get_item_name())
                    print("Category    :", item.get_category())
                    print("Location    :", item.get_location())
                    print("Date        :", item.get_date())
                    print("Status      :", item.get_status())
                    print("-" * 45)

            print("\n" + "=" * 45)
            print("             MY FOUND REPORTS")
            print("=" * 45)

            my_found_items = get_my_found_items(
                user.get_user_id()
            )

            if not my_found_items:

                print("No Found Reports")

            else:

                for item in my_found_items:

                    print("\n" + "-" * 45)
                    print("Found ID       :", item.get_found_id())
                    print("Lost ID        :", item.get_lost_id())
                    print("Found Date     :", item.get_found_date())
                    print("Found Location :", item.get_found_location())
                    print("Status         :", item.get_status())
                    print("-" * 45)

        # --------------------------------------------------
        # 6. LOGOUT
        # --------------------------------------------------

        elif choice == "6":

            print("Logging out...")
            break

        # --------------------------------------------------
        # 7. CONTACT FOUND ITEM
        # --------------------------------------------------

        elif choice == "7":

            found_id = input("Enter Found ID: ")

            result = get_contact_details(
                found_id,
                user.get_user_id()
            )

            if result is None:

                print("Found Item Not Found")

            elif result["role"] == "other":

                print(
                    "You are not the owner or finder of this item"
                )

            else:

                contact = result["contact"]

                print("Your Role:", result["role"])
                print("Contact Name:", contact["name"])
                print("Email:", contact["email"])
                print("Phone:", contact["phone"])

        # --------------------------------------------------
        # 8. CLAIM FOUND ITEM
        # --------------------------------------------------

        elif choice == "8":

            found_id = input("Enter Found ID: ")

            result = claim_found_item(
                found_id,
                user.get_user_id()
            )

            if result is True:

                print("Item Claimed Successfully")

            else:

                print(result)

        else:

            print("Invalid Choice! Please Try Again.")


def admin_menu(user):

    while True:

        print("\n" + "=" * 45)
        print("            ADMIN DASHBOARD")
        print("=" * 45)
        print("1. View Students")
        print("2. View Lost Items")
        print("3. View Found Items")
        print("4. View Statistics")
        print("5. Logout")
        print("=" * 45)

        choice = input("Enter Your Choice: ")

        # --------------------------------------------------
        # 1. VIEW STUDENTS
        # --------------------------------------------------

        if choice == "1":

            students = get_all_students()

            if not students:

                print("No Students Found")

            else:

                for student in students:

                    print("-" * 45)
                    print("Student ID :", student[0])
                    print("Name       :", student[1])
                    print("College ID :", student[2])
                    print("Email      :", student[3])
                    print("Phone      :", student[4])
                    print("-" * 45)

        # --------------------------------------------------
        # 2. VIEW LOST ITEMS
        # --------------------------------------------------

        elif choice == "2":

            lost_items = get_lost_items()

            if not display_lost_items(lost_items):

                print("No Lost Items Available")

        # --------------------------------------------------
        # 3. VIEW FOUND ITEMS
        # --------------------------------------------------

        elif choice == "3":

            found_items = get_found_items()

            if not display_found_items(found_items):

                print("No Found Items Available")

        # --------------------------------------------------
        # 4. VIEW STATISTICS
        # --------------------------------------------------

        elif choice == "4":

            statistics = get_statistics()

            if statistics is None:

                print("Unable To Load Statistics")

            else:

                print(
                    "Total Lost Reports :",
                    statistics["total_lost"]
                )

                print(
                    "Total Found Reports:",
                    statistics["total_found"]
                )

                print(
                    "Currently Lost     :",
                    statistics["currently_lost"]
                )

                print(
                    "Currently Found    :",
                    statistics["currently_found"]
                )

                print(
                    "Returned Items     :",
                    statistics["returned_items"]
                )

                print(
                    "Return Rate        :",
                    statistics["return_rate"],
                    "%"
                )

        # --------------------------------------------------
        # 5. LOGOUT
        # --------------------------------------------------

        elif choice == "5":

            print("Logging out...")
            break

        else:

            print("Invalid Choice! Please Try Again.")


# ==========================================================
# MAIN PROGRAM
# ==========================================================

while True:

    print("\n" + "=" * 45)
    print("       CAMPUS LOST & FOUND SYSTEM")
    print("=" * 45)
    print("1. Student Registration")
    print("2. Login")
    print("3. Exit")
    print("=" * 45)

    choice = input("Enter Your Choice: ")

    # ------------------------------------------------------
    # 1. STUDENT REGISTRATION
    # ------------------------------------------------------

    if choice == "1":

        name = input("Enter Name: ")
        college_id = input("Enter College ID: ")
        email = input("Enter Email: ")
        phone = input("Enter Phone: ")
        password = input("Enter Password: ")

        result = register_student(
            name,
            college_id,
            email,
            phone,
            password
        )

        if isinstance(result, str):

            print(result)

        else:

            print("\nRegistration Successful")
            print("Student ID:", result.get_user_id())

    # ------------------------------------------------------
    # 2. LOGIN
    # ------------------------------------------------------

    elif choice == "2":

        email = input("Enter Email: ")
        password = input("Enter Password: ")

        user = login(
            email,
            password
        )

        if user is None:

            print("Invalid Email or Password")

        else:

            print("\nLogin Successful")
            print("Welcome", user.get_name())

            if user.get_role() == "student":

                student_menu(user)

            elif user.get_role() == "admin":

                admin_menu(user)

    # ------------------------------------------------------
    # 3. EXIT
    # ------------------------------------------------------

    elif choice == "3":

        print("Thank You!")
        break

    else:

        print("Invalid Choice! Please Try Again.")
