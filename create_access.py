"""
User access configuration module for the User Access Control application.

This module defines the page permissions assigned to individual users.
It stores the relationship between usernames and the application pages
they are authorized to access.

Imports:
    get_connection: Provides a function to establish a connection
        to the MySQL database.

Global Variables:
    ACCESS (dict[str, list[str]]): Maps each username to a list of
        page names that the user is allowed to access.

Access Configuration:
    priti: Access to page1 and page2.
    yogesh: Access to page3.
    amit: Access to page4.
    admin: Access to all four pages.
    neha: Access to page1, page2, and page3.
    rahul: Access to page2 and page4.

Purpose:
    Provides predefined user access permissions for controlling
    which application pages each user can view.
"""

from app.db import get_connection

ACCESS = {
    "priti": ["page1", "page2"],
    "yogesh": ["page3"],
    "amit": ["page4"],
    "admin": ["page1", "page2", "page3", "page4"],
    "neha": ["page1", "page2", "page3"],
    "rahul": ["page2", "page4"],
}


"""
User page permission initialization script.

This script configures page-level access permissions for users based on
the ACCESS dictionary.

It connects to the MySQL database, retrieves each user's ID using their
username, removes their existing page permissions, and inserts the
updated permissions into the user_pages table.

Execution Flow:
    1. Establishes a connection to the MySQL database.
    2. Iterates through each username and its assigned pages in ACCESS.
    3. Searches the users table to retrieve the corresponding user ID.
    4. Skips the user if their username does not exist in the database.
    5. Deletes the user's previously assigned page permissions.
    6. Inserts the newly assigned pages into the user_pages table.
    7. Commits all database changes.
    8. Closes the database connection, even if an error occurs.

Database Tables:
    users:
        Stores user information, including user IDs and usernames.

    user_pages:
        Stores the relationship between users and their permitted pages.

Dependencies:
    get_connection: Establishes a MySQL database connection.
    ACCESS: Dictionary containing usernames and their assigned pages.

Important:
    Run create_users.py before executing this script to ensure that
    the required users exist in the database.

    Existing permissions for each processed user are replaced with
    the permissions specified in ACCESS.
"""

conn = get_connection()
try:
    with conn.cursor() as cur:
        for username, pages in ACCESS.items():
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            row = cur.fetchone()
            if not row:
                print(f"skip: user {username} not found (run create_users.py first)")
                continue
            cur.execute("DELETE FROM user_pages WHERE user_id = %s", (row["id"],))
            for page in pages:
                cur.execute("INSERT INTO user_pages (user_id, page_name) VALUES (%s, %s)", (row["id"], page))
            print(f"access set: {username} -> {pages}")
    conn.commit()
finally:
    conn.close()     