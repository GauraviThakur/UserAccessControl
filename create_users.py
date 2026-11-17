"""MEMBER A. Run once: python create_users.py  -> adds demo users with hashed passwords."""
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
