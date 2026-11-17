from app.db import get_connection 

ACCESS = {
    "priti": ["page1", "page2"],
    "yogesh" : ["page3"],
    "amit" : ["page4"],
    "admin" : ["page1", "page2", "page3", "page4"],
    "neha" : ["page1", "page2", "page3"],
    "rahul" : ["page2", "page4"],
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
            cur.execute("DELETE FROM user_page WHERE user_id = %s", (row["id"],))
            for page in pages:
                cur.execute("INSERT INTO user_page (user_id, page_name) VALUES (%s, %s)", (row["id"], page))
            print(f"access set: {username} -> {pages}")
    conn.commit()
finally:
    conn.close()     