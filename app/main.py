"""
Main module for the User Access Control application.

This module initializes and configures the FastAPI application,
loads environment variables, sets up session management, serves
static files, and registers application routers.

Application Setup:
    1. Loads environment variables from the .env file using load_dotenv().
    2. Imports authentication and access-control routers.
    3. Creates a FastAPI application instance.
    4. Adds SessionMiddleware to manage user sessions securely.
    5. Mounts the static directory to serve CSS, JavaScript, and other
       static files.
    6. Registers the authentication and access-control routers.

Environment Variables:
    SECRET_KEY (str): Secret key used by SessionMiddleware to sign
        session cookies. Uses a development default if not configured.

Modules:
    auth: Handles login, logout, and home page functionality.
    access: Handles page1-page4 routes and user access permissions.
    utils: Provides BASE_DIR for locating application resources.

Static Files:
    URL: /static
    Directory: BASE_DIR/static

Application:
    app: The main FastAPI application instance.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# Read .env first, so its values exist before the modules below are imported.
load_dotenv()

from . import auth, access  # noqa: E402  (imported after load_dotenv on purpose)
from .utils import BASE_DIR  # noqa: E402

# The application object that uvicorn runs.
app = FastAPI()

# Remember who is logged in. SECRET_KEY signs the cookie.
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "dev-secret-change-me"))

# Make style.css and access.css available at /static/...
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Join the routes written in the other files.
app.include_router(auth.router)     
app.include_router(access.router)   