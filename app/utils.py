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
    """Return the logged-in user row, or None. Login (Member A) sets session['user_id']."""
    user_id = request.session.get("user_id")
    return get_user_by_id(user_id) if user_id else None
