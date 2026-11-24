
Python Modules Documentation
============================

Introduction
------------

The application is divided into multiple Python modules. Each module
handles a specific responsibility to keep the code organized and maintainable.

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

auth.py
-------

The auth.py module handles authentication-related routes.

Responsibilities:

* Process user login requests.
* Verify user credentials.
* Create user sessions after successful login.
* Handle logout requests.
* Clear user sessions.

access.py
---------

The access.py module handles page-level authorization.

Responsibilities:

* Define or retrieve user page permissions.
* Check whether a user can access a requested page.
* Protect restricted pages.
* Handle unauthorized access.

db.py
-----

The db.py module handles database operations.

Responsibilities:

* Connect to the MySQL database.
* Retrieve user records.
* Retrieve user permissions.
* Perform database-related operations.

security.py
-----------

The security.py module handles password security.

Responsibilities:

* Generate password hashes using bcrypt.
* Verify passwords against stored hashes.

utils.py
--------

The utils.py module contains reusable helper functions.

Responsibilities:

* Provide common utility functionality.
* Avoid repeating shared logic across application modules.

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
