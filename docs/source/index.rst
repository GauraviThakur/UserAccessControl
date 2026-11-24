
User Access Control Documentation
=================================

Welcome to the documentation of the User Access Control project.

This project is developed using Python and FastAPI. It provides a secure
authentication and authorization system that allows users to log in and
access only the pages permitted to them.

Project Features
----------------

* User login and logout
* Password hashing using bcrypt
* Session-based authentication
* User-specific page permissions
* Protected routes using FastAPI
* MySQL database integration
* Access denied page for unauthorized users

Technology Stack
----------------

* Python
* FastAPI
* MySQL
* PyMySQL
* Starlette SessionMiddleware
* bcrypt
* HTML and CSS

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Project Documentation

   overview
   installation
   architecture
   database
   authentication
   authorization
   modules
   testing
   deployment
