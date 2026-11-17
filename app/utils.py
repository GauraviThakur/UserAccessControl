import os
from fastapi import Request
from .db import get_user_by_id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_html(file_name):
    """Read a plain .html file from app/html."""
    with open(os.path.join(BASE_DIR, "html", file_name), encoding="utf-8") as f:
        return f.read()


def current_user(request: Request):
    """Return the logged-in user row, or None. Login (Member A) sets session['user_id']."""
    user_id = request.session.get("user_id")
    return get_user_by_id(user_id) if user_id else None
