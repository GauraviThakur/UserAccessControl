
Authorization
=============

Introduction
------------

Authorization determines which resources an authenticated user is allowed
to access.

In the User Access Control application, each user has specific permissions
to access different pages.

Page-Level Access Control
-------------------------

The application uses user-specific page permissions.

For example:

.. code-block:: text

   Username    Page Permissions
   --------    ----------------
   priti       page1, page2
   yogesh      page3
   amit        page4
   admin       page1, page2, page3, page4
   neha        page1, page2, page3
   rahul       page2, page4

Permission Checking
-------------------

When a user requests a protected page, the application performs the following
checks:

1. Verify whether the user is logged in.
2. Retrieve the current user's information.
3. Retrieve the pages assigned to that user.
4. Check whether the requested page exists in the user's permissions.
5. Allow access if permission is available.
6. Otherwise, deny access.

Access Control Examples
-----------------------

Example 1: Authorized Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If Priti logs in and requests Page 1, access is granted because Page 1 is
included in her permissions.

Example 2: Unauthorized Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If Priti requests Page 3, access is denied because she does not have
permission to access that page.

Example 3: Administrator Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The administrator has permission to access all four protected pages.

Access Denied
-------------

When a user attempts to access a page without the required permission,
the application displays the access denied page.

Benefits
--------

* Prevents unauthorized page access.
* Provides user-specific permissions.
* Separates authentication from authorization.
* Makes access management easier.

Conclusion
----------

Authorization ensures that authenticated users can access only the pages
permitted to them.
