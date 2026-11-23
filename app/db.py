import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Create and return a connection to the MySQL database.

    Reads the database configuration from environment variables:
        DB_HOST: Database server hostname (default: localhost).
        DB_PORT: Database server port (default: 3306).
        DB_USER: Database username (default: root).
        DB_PASSWORD: Database password.
        DB_NAME: Database name (default: access_demo).

    Uses DictCursor so query results are returned as dictionaries,
    allowing columns to be accessed by their names.

    Returns:
        pymysql.connections.Connection: An active MySQL database connection.

    Raises:
        pymysql.MySQLError: If the database connection cannot be established.
        ValueError: If DB_PORT contains an invalid integer value.

    Example:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Kanchan@1234"),
        database=os.getenv("DB_NAME", "access_demo"),
        cursorclass=pymysql.cursors.DictCursor,
    )


def get_user_by_username(username):
    """
    Retrieve a user record from the database using their username.

    Establishes a database connection, executes a parameterized SQL query
    to find the matching user, and fetches the first matching record.

    Args:
        username (str): The username of the user to search for.

    Returns:
        dict | None: A dictionary containing the user's database record
        if a matching user is found; otherwise, None.

    Raises:
        pymysql.MySQLError: If a database operation fails.

    Example:
        user = get_user_by_username("admin")

        if user:
            print(user["username"])
        else:
            print("User not found.")
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cur.fetchone()
    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()
    finally:
        conn.close()
