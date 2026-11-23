"""MEMBER B: which user can open which page (page1 - page4)."""
from html import escape
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .db import get_connection
from .utils import load_html, current_user

router = APIRouter()

PAGES = ["page1", "page2", "page3", "page4"]



def get_user_pages(user_id):
    """
    Get all pages that a specific user is allowed to access.

    Args:
        user_id (int or str): Unique ID of the user.

    What it does:
        1. Connects to the database.
        2. Fetches all page names assigned to the given user_id
           from the user_pages table.
        3. Sorts the page names alphabetically.
        4. Closes the database connection.

    Returns:
        list[str]: A list of page names assigned to the user.
                   Returns an empty list if no pages are assigned.

    Example:
        Input:
            get_user_pages(101)

        Output:
            ['Attendance', 'Dashboard', 'Employee']
    """

    # Establish database connection
    conn = get_connection()

    try:
        # Create database cursor
        with conn.cursor() as cur:

            # Fetch all pages assigned to the user
            cur.execute(
                """
                SELECT page_name
                FROM user_pages
                WHERE user_id = %s
                ORDER BY page_name
                """,
                (user_id,)
            )

            # Extract page names and return them as a list
            pages = [row["page_name"] for row in cur.fetchall()]

            return pages

    finally:
        # Always close the database connection
        conn.close()



def make_page_route(page_name):
    def page_view(request: Request):
        user = current_user(request)
        if not user:
            return RedirectResponse("/login", status_code=303)

        # access check: is this page in this user's allowed list?
        if page_name not in get_user_pages(user["id"]):
            html = load_html("denied.html")
            html = html.replace("__NAME__", escape(user["full_name"]))
            html = html.replace("__PAGE__", page_name.replace("page", "Page "))
            return HTMLResponse(html, status_code=403)

        return HTMLResponse(load_html(page_name + ".html"))

    return page_view


for name in PAGES:
    router.add_api_route(f"/{name}", make_page_route(name), methods=["GET"], response_class=HTMLResponse)
