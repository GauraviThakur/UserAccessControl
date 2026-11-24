
Database Documentation
======================

Introduction
------------

The User Access Control application uses MySQL as its relational database
management system.

The database stores user information and page permission details required
for authentication and authorization.

Database Connectivity
---------------------

The application uses PyMySQL to connect Python code with the MySQL database.

The database module is responsible for managing database connections and
executing database-related operations.

Database Tables
---------------

Users Table
~~~~~~~~~~~

The users table stores registered user information.

Typical information includes:

* User ID
* Username
* Full name
* Password hash

User Permissions Table
~~~~~~~~~~~~~~~~~~~~~~

The user_pages table stores the pages that each user is allowed to access.

Typical information includes:

* User ID
* Page name

User Permission Relationship
----------------------------

A user can have permission to access multiple pages.

For example:

.. code-block:: text

   Username    Allowed Pages
   --------    --------------------
   priti       page1, page2
   yogesh      page3
   amit        page4
   admin       page1, page2, page3, page4

Database Operations
------------------

The application performs the following database operations:

* Establishing database connections.
* Retrieving user information.
* Verifying user credentials.
* Retrieving page permissions.
* Storing user and permission information.

Database Security
-----------------

The application should follow these database security practices:

* Use parameterized SQL queries.
* Do not store plain-text passwords.
* Keep database credentials in environment variables.
* Restrict database access to authorized users.
* Close database connections after use.

Conclusion
----------

The MySQL database provides persistent storage for user information and
page-level permissions.
