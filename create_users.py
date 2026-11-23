"""
User configuration module for the User Access Control application.

This module defines the initial user accounts that can be created
in the application's MySQL database.

It imports the database connection function and password hashing
function required for securely storing user credentials.

Imports:
    get_connection: Establishes a connection to the MySQL database.
    hash_password: Converts plain-text passwords into secure bcrypt hashes.

Global Variables:
    USERS (list[tuple[str, str, str]]): Stores the initial user details.
        Each tuple contains:
            - username: Unique username of the user.
            - full_name: Full name of the user.
            - password: Initial plain-text password to be hashed
              before storing it in the database.

Initial Users:
    - priti
    - yogesh
    - amit
    - admin
    - neha
    - rahul

Purpose:
    Provides predefined user information for initializing user
    accounts in the database.

Security:
    Passwords should never be stored directly in the database.
    Use hash_password() to generate bcrypt password hashes before
    inserting user records.
"""

from app.db import get_connection
from app.security import hash_password

USERS = [
    # username, full name, password
    ("priti", "Priti", "priti@123"),
    ("yogesh", "Yogesh", "yogesh@123"),
    ("amit", "Amit", "amit@123"),
    ("admin", "Admin", "admin@123"),
    ("neha", "Neha", "neha@123"),
    ("rahul", "Rahul", "rahul@123"),
]

conn = get_connection()
try:
    with conn.cursor() as cur:
        for username, full_name, password in USERS:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cur.fetchone():
                print(f"skip: {username} already exists")
                continue
            cur.execute(
                "INSERT INTO users (username, full_name, password_hash) VALUES (%s, %s, %s)",
                (username, full_name, hash_password(password)),
            )
            print(f"created: {username}")
    conn.commit()
finally:
    conn.close()
