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



def make_page_route(page_name: str) -> Callable[[Request], Union[RedirectResponse, HTMLResponse]]:
    """
    Create a page route with user authentication and authorization checks.

    Args:
        page_name (str): Name of the page to be accessed.
                         Example: "page1", "page2", "dashboard".

    What it does:
        1. Accepts a page name as input.
        2. Creates an inner function called page_view().
        3. When a user requests the page:
            a. Checks whether the user is logged in.
            b. If not logged in, redirects the user to the login page.
            c. Checks whether the requested page is in the user's
               allowed page list.
            d. If access is denied, displays the denied.html page
               with the user's name and requested page name.
            e. If access is allowed, loads and displays the
               requested HTML page.

    Returns:
        Callable[[Request], Union[RedirectResponse, HTMLResponse]]:
            Returns the inner page_view function.

            The inner function accepts a Request object and returns:
                - RedirectResponse: If the user is not logged in.
                - HTMLResponse: If access is denied or granted.

    Example:
        Input:
            make_page_route("page1")

        Returns:
            A page_view function that handles requests for page1.

    """

    def page_view(request: Request) -> Union[RedirectResponse, HTMLResponse]:
        """
        Handle the request and check user authentication and authorization.

        Args:
            request (Request): Incoming FastAPI HTTP request.

        Returns:
            RedirectResponse or HTMLResponse:
                Redirects to login or returns the appropriate HTML page.
        """

        # Step 1: Get the currently logged-in user
        user = current_user(request)

        # Step 2: Check whether the user is logged in
        if not user:
            return RedirectResponse("/login", status_code=303)

        # Step 3: Check whether the user has permission to access this page
        if page_name not in get_user_pages(user["id"]):

            # Load the access denied HTML page
            html = load_html("denied.html")

            # Replace the placeholder with the user's full name
            html = html.replace("__NAME__", escape(user["full_name"]))

            # Replace the placeholder with the requested page name
            html = html.replace("__PAGE__", page_name.replace("page", "Page "))

            # Return access denied response
            return HTMLResponse(html, status_code=403)

        # Step 4: User is authorized, so load the requested page
        return HTMLResponse(load_html(page_name + ".html"))

    # Step 5: Return the inner function
    return page_view

for name in PAGES:
    router.add_api_route(f"/{name}", make_page_route(name), methods=["GET"], response_class=HTMLResponse)
