
Project Overview
================

Introduction
------------

User Access Control is a web application developed using Python and FastAPI.
It provides authentication and authorization functionality to control which
pages a logged-in user can access.

The application verifies user credentials during login and uses session-based
authentication to maintain the user's login state.

Objectives
----------

* Provide secure user authentication.
* Store user information in a MySQL database.
* Protect application pages from unauthorized access.
* Assign different page permissions to different users.
* Display an access denied page when a user tries to access a restricted page.

Main Features
-------------

User Authentication
~~~~~~~~~~~~~~~~~~~

Users can log in using their username and password. Passwords are stored
as bcrypt hashes rather than plain text.

Session Management
~~~~~~~~~~~~~~~~~~

The application uses Starlette SessionMiddleware to maintain user login
sessions.

Page-Level Authorization
~~~~~~~~~~~~~~~~~~~~~~~~

Each user is assigned permission to access specific pages. The application
checks these permissions before displaying protected pages.

Technology Used
---------------

* Python 3.13
* FastAPI
* MySQL
* PyMySQL
* Starlette
* bcrypt
* HTML
* CSS

Application Pages
-----------------

The application includes the following protected pages:

* Page 1
* Page 2
* Page 3
* Page 4

The pages available to a user depend on the permissions assigned to that user.
