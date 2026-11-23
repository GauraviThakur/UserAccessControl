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
def login_form():
    return load_html("login.html").replace("__ERROR__", "")


@router.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user_by_username(username.strip())
    if not user or not verify_password(password, user["password_hash"]):
        error = '<p class="alert">Wrong username or password.</p>'
        return HTMLResponse(load_html("login.html").replace("__ERROR__", error), status_code=401)
    request.session.clear()
    request.session["user_id"] = user["id"]
    return RedirectResponse("/home", status_code=303)


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
