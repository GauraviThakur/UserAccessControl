"""
Utility functions for the User Access Control application.

This module provides common helper functions for locating application
resources, loading HTML templates, and retrieving the currently
authenticated user from the session.
"""

import os
from fastapi import Request
from .db import get_user_by_id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_html(file_name: str) -> str:
    """
    Read and return the contents of an HTML file from the app/html directory.

    Constructs the file path using BASE_DIR, opens the specified HTML
    file with UTF-8 encoding, and reads its contents.

    Args:
        file_name (str): Name of the HTML file to read.

    Returns:
        str: Contents of the HTML file as a string.

    Raises:
        FileNotFoundError: If the specified HTML file does not exist.
        OSError: If an error occurs while opening or reading the file.

    Example:
        html = load_html("login.html")
    """
    with open(os.path.join(BASE_DIR, "html", file_name), encoding="utf-8") as f:
        return f.read()


def current_user(request: Request):
    """
    Retrieve the currently logged-in user's database record.

    Reads the user_id from the request session and uses get_user_by_id()
    to retrieve the corresponding user record from the database.

    The login function (Member A) stores the user's ID in the session
    after successful authentication.

    Args:
        request (Request): The incoming FastAPI request containing
            the user's session information.

    Returns:
        dict | None: The logged-in user's database record if a valid
        user_id exists in the session; otherwise, None.

    Example:
        user = current_user(request)

        if user:
            print(user["username"])
        else:
            print("User is not logged in.")
    """
    user_id = request.session.get("user_id")
    return get_user_by_id(user_id) if user_id else None