Authentication
===============

Introduction
------------

Authentication is the process of verifying the identity of a user before
allowing access to the application.

The User Access Control application uses username and password authentication
with bcrypt password hashing.

Login Process
-------------

The login process follows these steps:

1. The user opens the login page.
2. The user enters a username and password.
3. The application receives the submitted credentials.
4. The application retrieves the corresponding user information from MySQL.
5. The submitted password is checked against the stored bcrypt password hash.
6. If the credentials are valid, the application creates a user session.
7. The user is redirected to the home page.
8. If the credentials are invalid, an error message is displayed.

Login Sequence Diagram
----------------------

.. mermaid::

   sequenceDiagram
       actor User
       participant Auth as auth.py
       participant DB as db.py (MySQL)
       participant Sec as security.py
       participant Session

       User->>Auth: POST /login (username, password)
       Auth->>DB: Get user by username
       DB-->>Auth: User record and password hash
       Auth->>Sec: verify_password(password, hash)
       Sec-->>Auth: True / False

       alt Valid credentials
           Auth->>Session: Store user ID
           Auth-->>User: Redirect to home
       else Invalid credentials
           Auth-->>User: Display login error
       end

Password Hashing
----------------

The application uses bcrypt to protect user passwords.

Password hashing converts a password into a secure hash before storing it
in the database.

During login, bcrypt verifies the submitted password against the stored hash.

Code Example
------------

The following example demonstrates password hashing and password verification.

.. code-block:: python

   from app.security import hash_password, verify_password

   # Generate a password hash during user registration
   stored_hash = hash_password("MySecret@123")

   # Verify the password during login
   is_valid = verify_password("MySecret@123", stored_hash)

   if is_valid:
       print("Login successful")
   else:
       print("Invalid password")

Session Management
------------------

The application uses Starlette SessionMiddleware to manage login sessions.

After successful login, the user's ID is stored in the session.

The session middleware manages the session cookie in the user's browser.

Session Configuration
~~~~~~~~~~~~~~~~~~~~~

The application configures session settings such as:

* Session secret key
* SameSite cookie policy
* HTTPS-only cookie setting
* Session expiration time

Logout Process
-------------

The logout process follows these steps:

1. The user selects the logout option.
2. The application clears the user's session.
3. The user is redirected to the login page.

Authentication Security
-----------------------

The following security practices are important:

* Store password hashes instead of plain-text passwords.
* Use a strong session secret.
* Configure secure cookies when deploying with HTTPS.
* Validate user input.
* Protect login routes against repeated password attempts.

Conclusion
----------

Authentication ensures that only users with valid credentials can log in
to the User Access Control application.