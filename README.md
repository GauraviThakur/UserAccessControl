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

## Project Structure

```text
User Access Control/
│
├── app/
│   ├── html/
│   ├── static/
│   ├── auth.py
│   ├── access.py
│   ├── db.py
│   ├── main.py
│   ├── security.py
│   └── utils.py
│
├── .env.example
├── .gitignore
├── create_users.py
├── requirements.txt
├── schema.sql
└── README.md
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

- **Member A:** Authentication, login, logout, user management, and session handling.
- **Member B:** Page-level access control and permission management.

## Security

- Passwords are stored as bcrypt hashes rather than plain text.
- Sessions are protected using signed cookies.
- SQL queries use parameterized statements.
- Backend permission checks protect restricted pages.
- User-provided text is escaped before being inserted into HTML.

## Project Status

Authentication and basic login functionality have been implemented and tested. Page-level permission integration and complete application testing are in progress.