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