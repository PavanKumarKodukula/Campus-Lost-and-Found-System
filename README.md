# Campus Lost & Found System

A Python-based console application that helps students report, find, claim, and manage lost and found items within a college campus. Built using Object-Oriented Programming (OOP) concepts with a **MySQL database** for data storage.

---

## 📌 Project Overview

The Campus Lost & Found System provides separate access for **Students** and **Admins**. Students can report lost items, report found items, view reports, contact the concerned person, and claim found items. Admins can view students, lost items, found items, and system-wide statistics.

**Item lifecycle:**

```
LOST → FOUND → RETURNED
```

- **LOST** – a student reports an item as lost.
- **FOUND** – another student finds the item and reports it.
- **RETURNED** – the verified owner claims the found item.

---

## ✨ Features

### Student
- Registration with automatic student ID generation
- Duplicate College ID / email validation
- Login
- Report lost items
- Report found items
- View all lost / found items
- View personal lost / found reports
- Contact the owner or finder
- Claim found items (owner-verified)
- Logout

### Admin
- Login
- View registered students
- View lost items
- View found items
- View system statistics (total reports, currently lost/found, returned items, return rate)
- Logout

> Note: The current version does not include admin operations for editing or deleting item records.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3 |
| Paradigm | Object-Oriented Programming (OOP) |
| Data Storage | MySQL database (`mysql-connector-python`) |
| Configuration | `.env` file (`python-dotenv`) |
| Interface | Console-based (no GUI/web frontend yet) |

---

## 🏗️ Project Structure

```
campus_lost_and_found/
│
├── models/
│   ├── user.py          # Base User class
│   ├── student.py       # Student (inherits User)
│   ├── admin.py         # Admin (inherits User)
│   ├── lost_item.py     # LostItem model
│   └── found_item.py    # FoundItem model
│
├── services/
│   ├── auth_service.py         # Registration, login, student management
│   ├── lost_item_service.py    # Lost item reporting & retrieval
│   ├── found_item_service.py   # Found item reporting, claiming, contact
│   └── statistics_service.py   # System statistics
│
├── connection.py         # MySQL connection, auto DB/table creation, default admin seed
├── .env                   # Database credentials (not committed)
├── requirements.txt
└── main.py
```

**Architecture:** `main.py` → User Interface → Service Layer (Auth / Lost Item / Found Item / Statistics) → Model Layer (User → Student/Admin, LostItem, FoundItem) → MySQL Database (via `connection.py`).

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.x installed
- MySQL Server installed and running

Check your Python version:
```bash
python --version
```

### 1. Clone or download the project
```bash
git clone <repository-url>
cd campus_lost_and_found
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
This installs `mysql-connector-python` and `python-dotenv`.

### 3. Configure the database connection
Create a `.env` file in the project root (a sample is provided) with your MySQL credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=campus_lost_found
```
> ⚠️ `.env` is listed in `.gitignore` so your credentials are never committed to GitHub.

### 4. Run the application
```bash
python main.py
```
On first run, `connection.py` automatically:
- Connects to your MySQL server
- Creates the `campus_lost_found` database if it doesn't exist
- Creates the `users`, `lost_items`, and `found_items` tables if they don't exist
- Seeds a default admin account (`A001`) if one isn't already present

No manual table creation or CSV setup is required.

### 5. Use the menu
```
CAMPUS LOST & FOUND SYSTEM

1. Student Registration
2. Login
3. Exit
```

### Default Admin Login
There is no admin registration flow in the app (the main menu only offers **Student Registration**). A default admin account is auto-created on first run:
```
Email:    admin@campus.com
Password: admin@123
```
> ⚠️ Passwords are stored in plain text in the database, so change this default password in a real deployment.

---

## 🗄️ Database Notes

- **MySQL** is used for persistence, accessed through `mysql-connector-python`. No CSV files or REST API are used in this version.
- Connection details are read from environment variables via `.env` (`python-dotenv`), keeping credentials out of source control.
- `connection.py` handles first-run setup: creating the database, creating tables, and seeding the default admin — no manual SQL scripts to run.
- **Tables:**
  - `users` — student and admin account records
  - `lost_items` — all reported lost items and their status
  - `found_items` — all reported found items, linked to lost items by ID, and their status
- ⚠️ Passwords are currently stored in plain text in the `users` table; this is a known limitation (see below).

---

## 🧠 OOP Concepts Demonstrated

- **Classes & Objects** — `User`, `Student`, `Admin`, `LostItem`, `FoundItem`
- **Inheritance** — `Student(User)` and `Admin(User)`
- **Encapsulation** — private attributes (e.g. `self.__user_id`, `self.__status`) with getters/setters
- **Constructors** — `__init__()` initializes object state
- **`super()`** — used by `Student` and `Admin` to call the parent `User` constructor

---

## ⚠️ Current Limitations

- Passwords stored in plain text (not hashed)
- Console-based only; no GUI or web frontend
- No image upload support for items
- Query results in some admin views are accessed by column position rather than column name

## 🔮 Future Enhancements

- Password hashing for stored credentials
- Flask REST API
- Web-based frontend
- Email notifications
- Search and filtering
- Admin item management (edit/delete)
- Smarter lost–found item matching
- Deploy for campus-wide access

---

## 👥 Team Member Contributions

| Name | Role / Contribution |
|---|---|
| Pavan | `LostItem` model, lost item service (report lost item, retrieve/list/update status, per-user lost reports), statistics service (system-wide counts and return rate) — migrated to MySQL queries. Also added the MySQL connection setup (`connection.py`: database/table creation, default admin seeding), `requirements.txt`, and `.gitignore` |
| Venkat | Core models (`User`, `Student`, `Admin`), authentication service (registration, login, duplicate ID/email checks, student lookup), and `main.py` console UI / menu flow for both roles — migrated to MySQL queries |
| Vignesh | `FoundItem` model and found item service (report found item, claim/return workflow, contact-details lookup between owner and finder) — migrated to MySQL queries |
