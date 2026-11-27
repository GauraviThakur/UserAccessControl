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

Architecture Diagram
--------------------

The diagram below shows how a browser request moves through the
application components.

.. mermaid::

   flowchart TD
       U[User Browser] -->|HTTP Request| M[main.py<br/>FastAPI App]
       M --> SM[SessionMiddleware]
       M --> A[auth.py<br/>Login / Logout]
       M --> AC[access.py<br/>Page Permissions]
       A --> S[security.py<br/>bcrypt Hashing]
       A --> D[(db.py<br/>MySQL Database)]
       AC --> D
       A --> UT[utils.py]
       AC --> UT
       M --> H[html/<br/>Templates]
       M --> ST[static/<br/>CSS]

Module Dependency Diagram
-------------------------

The diagram below shows which modules depend on which other modules.

.. mermaid::

   classDiagram
       class main {
           +app
           +include_router()
           +mount_static()
       }
       class auth {
           +login()
           +logout()
       }
       class access {
           +get_user_pages()
           +check_page_access()
       }
       class db {
           +get_connection()
           +get_user()
           +get_user_permissions()
       }
       class security {
           +hash_password()
           +verify_password()
       }
       class utils {
           +helper functions
       }
       main --> auth
       main --> access
       auth --> db
       auth --> security
       access --> db
       auth --> utils
       access --> utils

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

Login Sequence Diagram
~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
       actor User
       participant Auth as auth.py
       participant Sec as security.py
       participant DB as db.py (MySQL)
       User->>Auth: POST /login (username, password)
       Auth->>DB: get_user(username)
       DB-->>Auth: user record + password hash
       Auth->>Sec: verify_password(password, hash)
       Sec-->>Auth: True / False
       alt valid credentials
           Auth-->>User: create session, redirect to home.html
       else invalid credentials
           Auth-->>User: show login.html with error
       end

Page Access Sequence Diagram
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
       actor User
       participant Main as main.py
       participant Acc as access.py
       participant DB as db.py
       User->>Main: GET /page1
       Main->>Acc: check_page_access(session user, "page1")
       Acc->>DB: get_user_permissions(user)
       DB-->>Acc: allowed pages
       alt page allowed
           Acc-->>User: page1.html
       else not allowed
           Acc-->>User: denied.html
       end

Conclusion
----------

The modular architecture makes the application easier to understand,
maintain, test, and extend.