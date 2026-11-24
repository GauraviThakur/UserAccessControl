
Testing Documentation
=====================

Introduction
------------

Testing verifies that the User Access Control application works correctly
and prevents unauthorized access.

Authentication Testing
----------------------

Login with Valid Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open the login page.
2. Enter a valid username and password.
3. Submit the login form.
4. Verify that the user is redirected to the home page.

Expected Result: The user should log in successfully.

Login with Invalid Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open the login page.
2. Enter an incorrect username or password.
3. Submit the login form.

Expected Result: The application should reject the login attempt.

Logout Testing
--------------

1. Log in to the application.
2. Select the logout option.
3. Try opening a protected page.

Expected Result: The user should be redirected to the login page or denied
access.

Authorization Testing
---------------------

Authorized Page Access
~~~~~~~~~~~~~~~~~~~~~~

1. Log in as Priti.
2. Open Page 1 or Page 2.

Expected Result: Access should be granted.

Unauthorized Page Access
~~~~~~~~~~~~~~~~~~~~~~~~

1. Log in as Priti.
2. Try opening Page 3.

Expected Result: Access should be denied.

Administrator Access
~~~~~~~~~~~~~~~~~~~~

1. Log in as Admin.
2. Open Page 1, Page 2, Page 3, and Page 4.

Expected Result: Access should be granted to all four pages.

Session Testing
---------------

Verify that:

* A logged-in user's session is maintained while navigating pages.
* The session expires according to the configured expiration time.
* Logout clears the session.

Database Testing
----------------

Verify that:

* User records can be retrieved from MySQL.
* Password hashes are stored correctly.
* User page permissions are retrieved correctly.

Conclusion
----------

Testing helps identify errors and ensures that authentication, authorization,
session management, and database operations work as expected.
