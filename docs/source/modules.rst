Python Modules Documentation
============================

Introduction
------------

The application is divided into multiple Python modules. Each module
handles a specific responsibility to keep the code organized and maintainable.

Module Dependency Diagram
-------------------------

.. mermaid::

   flowchart LR
       main[main.py] --> auth[auth.py]
       main --> access[access.py]
       main --> db[db.py]
       auth --> db
       auth --> security[security.py]
       access --> db
       auth --> utils[utils.py]
       access --> utils

main.py
-------

The main.py module is the entry point of the FastAPI application.

Responsibilities:

* Create the FastAPI application instance.
* Initialize the database.
* Configure SessionMiddleware.
* Mount static files.
* Register authentication and page routers.
* Configure application exception handling.

**Example usage**

.. code-block:: python

   # Run the application from the project root
   #   uvicorn app.main:app --reload

   from fastapi import FastAPI
   from starlette.middleware.sessions import SessionMiddleware

   app = FastAPI()
   app.add_middleware(SessionMiddleware, secret_key="change-this-secret")

**API reference**

.. automodule:: app.main
   :members:
   :undoc-members:

auth.py
-------

The auth.py module handles authentication-related routes.

Responsibilities:

* Process user login requests.
* Verify user credentials.
* Create user sessions after successful login.
* Handle logout requests.
* Clear user sessions.

**Example usage**

.. code-block:: python

   # POST /login  (form fields: username, password)
   #
   # Valid credentials   -> user ID stored in session, redirect to home page
   # Invalid credentials -> login.html shown again with an error message
   #
   # GET /logout
   #
   # Session cleared -> redirect to login page

**API reference**

.. automodule:: app.auth
   :members:
   :undoc-members:

access.py
---------

The access.py module handles page-level authorization.

Responsibilities:

* Define or retrieve user page permissions.
* Check whether a user can access a requested page.
* Protect restricted pages.
* Handle unauthorized access.

**Example usage**

.. code-block:: python

   from app.access import check_page_access

   if check_page_access(username="priti", page="page1"):
       print("Show page1.html")      # Priti has page1 permission
   else:
       print("Show denied.html")

   check_page_access("priti", "page3")   # False -> denied.html
   check_page_access("admin", "page3")   # True  -> page3.html

**API reference**

.. automodule:: app.access
   :members:
   :undoc-members:

db.py
-----

The db.py module handles database operations.

Responsibilities:

* Connect to the MySQL database.
* Retrieve user records.
* Retrieve user permissions.
* Perform database-related operations.

**Example usage**

.. code-block:: python

   from app.db import get_connection

   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT username FROM users WHERE username = %s", ("priti",))
   print(cursor.fetchone())
   conn.close()

**API reference**

.. automodule:: app.db
   :members:
   :undoc-members:

security.py
-----------

The security.py module handles password security.

Responsibilities:

* Generate password hashes using bcrypt.
* Verify passwords against stored hashes.

**Example usage**

.. code-block:: python

   from app.security import hash_password, verify_password

   hashed = hash_password("MySecret@123")
   print(verify_password("MySecret@123", hashed))   # True
   print(verify_password("wrong", hashed))          # False

**API reference**

.. automodule:: app.security
   :members:
   :undoc-members:

utils.py
--------

The utils.py module contains reusable helper functions.

Responsibilities:

* Provide common utility functionality.
* Avoid repeating shared logic across application modules.

**Example usage**

.. code-block:: python

   from app.utils import some_helper

   result = some_helper("input value")

**API reference**

.. automodule:: app.utils
   :members:
   :undoc-members:

HTML Templates
--------------

The application uses HTML templates to display its user interface.

login.html
~~~~~~~~~~

Displays the login form.

home.html
~~~~~~~~~

Displays the home page after successful login.

denied.html
~~~~~~~~~~~

Displays an access denied message.

page1.html to page4.html
~~~~~~~~~~~~~~~~~~~~~~~~

These are protected pages displayed according to user permissions.

Static Files
------------

The static directory contains CSS files used to style the application's
HTML pages.

Conclusion
----------

Separating responsibilities into different modules improves readability,
maintainability, and code reuse.