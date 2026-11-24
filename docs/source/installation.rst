
Installation Guide
==================

Prerequisites
-------------

Before running the application, make sure the following software is installed:

* Python 3.13
* MySQL Server
* MySQL client or MySQL Workbench
* Visual Studio Code or another code editor

Download the Project
--------------------

Open the project folder in your terminal.

Install Required Packages
-------------------------

Create a virtual environment:

.. code-block:: bash

   python -m venv venv

Activate the virtual environment on Windows:

.. code-block:: bat

   venv\Scripts\activate

Install the required Python packages:

.. code-block:: bash

   python -m pip install fastapi uvicorn pymysql bcrypt python-dotenv itsdangerous

Database Configuration
----------------------

Make sure MySQL Server is running.

Create the database and configure the database connection according to the
settings used by the application's database module.

Environment Configuration
-------------------------

Configure the required environment variables, such as database credentials
and session secret, according to the project's configuration.

Run the Application
-------------------

Start the FastAPI application using:

.. code-block:: bash

   python -m uvicorn app.main:app --reload

Open the following URL in your browser:

.. code-block:: text

   http://127.0.0.1:8000

API Documentation
-----------------

FastAPI provides interactive API documentation at:

.. code-block:: text

   http://127.0.0.1:8000/docs
