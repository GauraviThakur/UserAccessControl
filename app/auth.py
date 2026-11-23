"""
Authentication module for the User Access Control application.

This module defines the authentication API router and imports the
functions required to handle user login, logout, session management,
and home page functionality.

It uses FastAPI form handling, database queries, password verification,
and session-based authentication to manage user access.

Imports:
    escape: Escapes special HTML characters to help prevent HTML injection.
    APIRouter: Creates a router for registering authentication endpoints.
    Request: Provides access to request data and session information.
    Form: Extracts form data submitted by users.
    HTMLResponse: Returns HTML content as an HTTP response.
    RedirectResponse: Redirects users to another URL.
    Response: Base response class for HTML and redirect responses.
    get_user_by_username: Retrieves a user record using their username.
    verify_password: Checks the entered password against the stored hash.
    load_html: Loads HTML templates from the application's HTML directory.
    current_user: Retrieves the currently logged-in user's database record.
    get_user_pages: Retrieves the pages assigned to a user.

Global Variables:
    router (APIRouter): Router used to register authentication endpoints.

Authentication Features:
    - User login and password verification.
    - Session management after successful login.
    - Logout and session clearing.
    - Home page access for authenticated users.
    - Retrieving user-specific page permissions.
"""

from html import escape
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.responses import Response

from .db import get_user_by_username
from .security import verify_password
from .utils import load_html, current_user
from .access import get_user_pages  # written by Member B: returns e.g. ["page1", "page2"]

router = APIRouter()



@router.get("/")
def root(request: Request) -> RedirectResponse:
    """
    Handle requests to the root URL ("/") and redirect users
    based on their login status.

    Args:
        request (Request): Incoming HTTP request object.
                           Contains the user's session information.

    What it does:
        1. Receives a request when the user visits the root URL.
        2. Checks whether the user's session contains a "user_id".
        3. If user_id exists, redirects the user to "/home".
        4. If user_id does not exist, redirects the user to "/login".
        5. Uses HTTP status code 303 to perform the redirect.

    Returns:
        RedirectResponse: Redirects the user to either:
                          - "/home" if the user is logged in.
                          - "/login" if the user is not logged in.

    Example:
        Logged-in user:
            GET /
            Redirects to /home

        Not logged-in user:
            GET /
            Redirects to /login
    """

    return RedirectResponse(
        "/home" if request.session.get("user_id") else "/login",
        status_code=303
    )



@router.get("/login", response_class=HTMLResponse)
def login_form() -> HTMLResponse:
    """
    Display the login page to the user.

    Args:
        None: This function does not require any input parameters.

    What it does:
        1. Handles GET requests to the "/login" URL.
        2. Loads the login.html file.
        3. Replaces the "__ERROR__" placeholder with an empty string.
           This ensures that no error message is displayed initially.
        4. Returns the updated HTML content as a response.

    Returns:
        HTMLResponse: Returns the login page HTML content
                      with the error message placeholder cleared.

    Example:
        Request:
            GET /login

        Output:
            Displays the login page without an error message.
    """

    return HTMLResponse(
        load_html("login.html").replace("__ERROR__", "")
    )



@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
) -> Response:
    """
    Authenticate a user using their username and password.

    Args:
        request (Request): Incoming HTTP request object.
                           Used to access and manage the user session.

        username (str): Username entered in the login form.
                        Required form field.

        password (str): Password entered in the login form.
                        Required form field.

    What it does:
        1. Receives the username and password submitted through
           the login form.
        2. Removes leading and trailing whitespace from the username.
        3. Fetches the user details from the database using
           get_user_by_username().
        4. Checks whether the user exists.
        5. Verifies the entered password against the stored
           password hash using verify_password().
        6. If the username or password is incorrect:
           - Displays an error message.
           - Returns the login page with HTTP status code 401.
        7. If authentication is successful:
           - Clears the existing session.
           - Stores the user's ID in the session.
           - Redirects the user to the home page.

    Returns:
        HTMLResponse | RedirectResponse:
            HTMLResponse: Returns the login page with an error
                          message if authentication fails.

            RedirectResponse: Redirects the authenticated user
                              to "/home" with HTTP status code 303.

    Example:
        Input:
            username = "admin"
            password = "admin123"

        Successful login:
            Redirects to "/home".

        Failed login:
            Displays "Wrong username or password."
            and returns HTTP 401.
    """

    # Fetch user details using the username
    user = get_user_by_username(username.strip())

    # Verify username and password
    if not user or not verify_password(password, user["password_hash"]):

        # Prepare login error message
        error = '<p class="alert">Wrong username or password.</p>'

        # Return login page with error message
        return HTMLResponse(
            load_html("login.html").replace("__ERROR__", error),
            status_code=401
        )

    # Clear the existing session
    request.session.clear()

    # Store authenticated user's ID in the session
    request.session["user_id"] = user["id"]

    # Redirect successfully authenticated user to home page
    return RedirectResponse(
        "/home",
        status_code=303
    )



@router.get("/logout")
def logout(request: Request) -> RedirectResponse:
    """
    Log out the currently authenticated user.

    Args:
        request (Request): Incoming HTTP request object.
                           Used to access and manage the user's session.

    What it does:
        1. Handles GET requests to the "/logout" URL.
        2. Clears all data stored in the user's session.
        3. Removes the user's login information from the session.
        4. Redirects the user to the login page.
        5. Uses HTTP status code 303 for redirection.

    Returns:
        RedirectResponse: Redirects the user to "/login"
                          after clearing the session.

    Example:
        Request:
            GET /logout

        Output:
            Clears the user session and redirects to "/login".
    """

    # Clear all session data
    request.session.clear()

    # Redirect the user to the login page
    return RedirectResponse(
        "/login",
        status_code=303
    )



@router.get("/home", response_class=HTMLResponse)
def home(request: Request) -> Response:
    """
    Display the home page with the logged-in user's details
    and assigned page links.

    Args:
        request (Request): Incoming HTTP request object.
                           Used to identify the currently logged-in user
                           and access session information.

    What it does:
        1. Handles GET requests to the "/home" URL.
        2. Checks whether the user is logged in using current_user().
        3. If the user is not logged in, redirects them to "/login".
        4. Retrieves the list of pages assigned to the user
           using get_user_pages().
        5. If the user has assigned pages:
           - Generates HTML list items containing links to each page.
           - Replaces "page" in page names with "Page " for display.
        6. If no pages are assigned, displays a message:
           "No pages assigned to you yet."
        7. Loads the home.html template.
        8. Replaces the "__NAME__" placeholder with the user's
           escaped full name.
        9. Replaces the "__LINKS__" placeholder with the generated
           page links or the no-pages message.
        10. Returns the updated home page as an HTML response.

    Returns:
        Response:
            RedirectResponse: Redirects unauthenticated users
                              to "/login" with status code 303.

            HTMLResponse: Displays the home page with the user's
                          name and assigned page links.

    Example:
        Logged-in user with assigned pages:
            Displays the home page with the user's name
            and available page links.

        Logged-in user without assigned pages:
            Displays "No pages assigned to you yet."

        Unauthenticated user:
            Redirects to "/login".
    """

    # Get the currently logged-in user
    user = current_user(request)

    # Redirect to login if the user is not authenticated
    if not user:
        return RedirectResponse("/login", status_code=303)

    # Retrieve all pages assigned to the user
    pages = get_user_pages(user["id"])

    # Generate HTML links for assigned pages
    if pages:
        links = "".join(
            f'<li><a href="/{p}">{p.replace("page", "Page ")}</a></li>'
            for p in pages
        )
    else:
        # Display a message if no pages are assigned
        links = "<li>No pages assigned to you yet.</li>"

    # Load the home page HTML template
    html = load_html("home.html")

    # Replace placeholders with user details and page links
    html = html.replace(
        "__NAME__", escape(user["full_name"])
    ).replace(
        "__LINKS__", links
    )

    # Return the updated home page
    return HTMLResponse(html)

