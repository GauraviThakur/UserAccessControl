
System Architecture
===================

Introduction
------------

The User Access Control application follows a modular architecture.
The application separates authentication, authorization, database operations,
security, and utility functions into different Python modules.

Application Structure
---------------------

The project contains the following main components:

.. code-block:: text

   UserAccessControl/
   |
   +-- app/
   |   |
   |   +-- main.py
   |   +-- auth.py
   |   +-- access.py
   |   +-- db.py
   |   +-- security.py
   |   +-- utils.py
   |   |
   |   +-- html/
   |   |   +-- login.html
   |   |   +-- home.html
   |   |   +-- denied.html
   |   |   +-- page1.html
   |   |   +-- page2.html
   |   |   +-- page3.html
   |   |   +-- page4.html
   |   |
   |   +-- static/
   |
   +-- docs/
       +-- source/
       +-- build/

Main Components
---------------

main.py
~~~~~~~

The main application module creates the FastAPI application, configures
session middleware, mounts static files, initializes the database, and
registers application routes.

auth.py
~~~~~~~

This module handles user authentication, including login and logout
functionality.

access.py
~~~~~~~~~

This module manages user-specific page permissions and controls access
to protected pages.

db.py
~~~~~

This module handles database connectivity and database-related operations.

security.py
~~~~~~~~~~~

This module contains security-related functionality, such as password
hashing and password verification.

utils.py
~~~~~~~~

This module contains reusable helper functions used by the application.

Authentication and Authorization Flow
-------------------------------------

The application follows this general workflow:

1. The user opens the login page.
2. The user submits their username and password.
3. The application verifies the credentials.
4. After successful authentication, a user session is created.
5. The user opens a protected page.
6. The application checks the user's page permissions.
7. If permission is granted, the requested page is displayed.
8. Otherwise, the access denied page is displayed.

Conclusion
----------

The modular architecture makes the application easier to understand,
maintain, test, and extend.
