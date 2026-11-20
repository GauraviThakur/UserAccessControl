# User Access Control System

## Project Overview

The User Access Control System is a web-based application developed using Python, FastAPI, and MySQL. It provides secure login functionality and controls which pages a user can access based on their assigned permissions.

After successful login, users are redirected to a home page where they can see only the pages they are authorized to access.

The application also verifies permissions on the backend to prevent unauthorized access through manually entered URLs.

## Technologies Used

- Python
- FastAPI
- MySQL
- PyMySQL
- HTML
- CSS
- bcrypt
- Starlette Session Middleware

## Key Features

- User login and logout.
- Secure password storage using bcrypt hashing.
- Session-based authentication.
- User-specific page permissions.
- Dynamic display of authorized pages on the home page.
- Backend permission verification for protected pages.
- Access denied response for unauthorized requests.
- MySQL database integration.

## Application Workflow

1. The user opens the application.
2. The application redirects the user to the login page if they are not authenticated.
3. The user enters their username and password.
4. The application retrieves the user's details from the MySQL database.
5. The entered password is verified against the stored bcrypt hash.
6. If authentication succeeds, the user's ID is stored in the session.
7. The user is redirected to the home page.
8. The home page displays the pages assigned to that user.
9. When a user opens a protected page, the backend checks whether the user has permission.
10. The user can log out, which clears the session.

## Authentication and Session Management

The authentication module is responsible for handling login, logout, and the home page.

### Login Authentication

- User credentials are submitted through an HTML login form.
- The username is used to retrieve the corresponding user record from the database.
- The entered password is verified using bcrypt.
- A generic error message is displayed when the username or password is incorrect.
- On successful authentication, the session is cleared and the authenticated user's ID is stored in it.

### Password Security

Passwords are not stored as plain text.

The application uses bcrypt to:
- Generate a secure password hash when creating demo users.
- Verify entered passwords against their stored hashes during login.

### Session Management

Starlette Session Middleware manages user sessions using signed cookies.

The application stores the authenticated user's ID in the session. This allows the application to identify the logged-in user when they access other routes.

When the user logs out, the session is cleared.

### Home Page and User Permissions

After login, the application retrieves the user's assigned page names through the `get_user_pages()` function.

The returned page names are used to generate links dynamically on the home page.

Displaying a link does not itself grant access. The backend separately verifies permissions whenever a protected page is requested.

## Database Integration

The application uses MySQL as its database.

The `users` table stores user information, including:

- User ID
- Username
- Full name
- Password hash

PyMySQL is used to establish database connections and execute SQL queries.

Parameterized SQL statements are used when retrieving and inserting user information.

## Project Structure

```text
User Access Control/
|
|-- app/
|   |-- html/
|   |   |-- home.html
|   |   |-- login.html
|   |
|   |-- static/
|   |   |-- style.css
|   |   |-- access.css
|   |
|   |-- auth.py
|   |-- access.py
|   |-- db.py
|   |-- main.py
|   |-- security.py
|   |-- utils.py
|
|-- .env
|-- .env.example
|-- .gitignore
|-- create_users.py
|-- requirements.txt
|-- schema.sql
|-- README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/GauraviThakur/UserAccessControl.git
cd UserAccessControl
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure the MySQL connection details and a strong secret key.

### 5. Create the Database and Users Table

Run the SQL script:

```bash
mysql -u root -p < schema.sql
```

### 6. Create Demo Users

```bash
python create_users.py
```

### 7. Run the Application

```bash
python -m uvicorn app.main:app --reload
```

Open the application at:

```text
http://127.0.0.1:8000
```

## Team Contribution

This project is developed collaboratively.

**Member A – Authentication**
- Login and logout functionality.
- Password hashing and verification.
- Session management.
- Home page and dynamic display of assigned page links.
- User table schema and demo user creation.

**Member B – Access Control**
- Page-level access control.
- User-to-page permission management.
- Backend authorization checks for protected pages.
- Access denied handling.

**Shared Responsibilities**
- Application entry point and router integration.
- Database connection and shared utilities.
- Project integration and testing.

## Security

- Passwords are stored as bcrypt hashes rather than plain text.
- Sessions are protected using signed cookies.
- SQL queries use parameterized statements.
- Backend permission checks protect restricted pages.
- User-provided text is escaped before being inserted into HTML.
- Unauthenticated users are redirected to the login page.
- Unauthorized access to protected pages is rejected by the backend.

## Project Status

The authentication module has been implemented and tested, including login, logout, password verification, session handling, and home page functionality.

Page-level permission management and integration between authentication and access control are being developed collaboratively.

