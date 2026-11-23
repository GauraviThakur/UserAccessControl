"""MEMBER A: login, logout and home page."""
from html import escape
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

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
) -> HTMLResponse | RedirectResponse:
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
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


@router.get("/home", response_class=HTMLResponse)
def home(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    pages = get_user_pages(user["id"])
    if pages:
        links = "".join(f'<li><a href="/{p}">{p.replace("page", "Page ")}</a></li>' for p in pages)
    else:
        links = "<li>No pages assigned to you yet.</li>"

    html = load_html("home.html")
    html = html.replace("__NAME__", escape(user["full_name"])).replace("__LINKS__", links)
    return HTMLResponse(html)
