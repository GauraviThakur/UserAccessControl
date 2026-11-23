"""MEMBER B: which user can open which page (page1 - page4)."""
from html import escape
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .db import get_connection
from .utils import load_html, current_user

from collections.abc import Callable
from starlette.responses import Response

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
        


def make_page_route(page_name: str) -> Callable[[Request], Response]:
    """
    Create a page route handler with authentication
    and authorization checks.

    Args:
        page_name (str): Name of the HTML page to access.
                         Example: "page1", "page2", "dashboard".

    What it does:
        1. Creates an inner function named page_view().
        2. Checks whether the user is logged in.
        3. Redirects unauthenticated users to the login page.
        4. Checks whether the requested page is assigned
           to the logged-in user.
        5. If access is denied, displays the denied.html page.
        6. If access is allowed, displays the requested HTML page.

    Returns:
        Callable[[Request], Response]:
            Returns a page_view function that accepts an HTTP
            Request and returns an HTTP Response.

    Example:
        make_page_route("page1")

        Returns a page handler for page1.
    """

    def page_view(request: Request) -> Response:

        # Get the currently logged-in user
        user = current_user(request)

        # Redirect if the user is not logged in
        if not user:
            return RedirectResponse(
                "/login",
                status_code=303
            )

        # Check whether the user has permission to access the page
        if page_name not in get_user_pages(user["id"]):

            # Load the access-denied HTML page
            html = load_html("denied.html")

            # Insert the user's name
            html = html.replace(
                "__NAME__",
                escape(user["full_name"])
            )

            # Insert the requested page name
            html = html.replace(
                "__PAGE__",
                page_name.replace("page", "Page ")
            )

            # Return forbidden response
            return HTMLResponse(
                html,
                status_code=403
            )

        # Return the requested HTML page
        return HTMLResponse(
            load_html(page_name + ".html")
        )

    return page_view


for name in PAGES:
    router.add_api_route(f"/{name}", make_page_route(name), methods=["GET"], response_class=HTMLResponse)
