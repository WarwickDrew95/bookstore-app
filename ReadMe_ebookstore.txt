Key Features
____________________________________________________________________
Login:

To sign in as admin-
Username: admin
Password: adm1n

Only admin user can add nuw users.
--------------------------------------------------------------------

Add new books:

Update book information (title, author, or quantity)

Delete books by ID

Search for books by ID or title keyword
____________________________________________________________________

Admin Functions:
--------------------------------------------------------------------

Add new employee accounts

Reset user passwords
____________________________________________________________________

Reporting Tools:
--------------------------------------------------------------------
Low stock alert on login (books with quantity < 5)

Export inventory report to a readable .txt file
____________________________________________________________________

First-Time Login Instructions
Run the Python script:
--------------------------------------------------------------------

bash
Copy
Edit
python bookstore_dat.py
At the login prompt, use the default admin credentials:

Username: admin

Password: adm1n

Once logged in as admin, you can:

View books low in stock

Access all menu features

Create accounts for other users (employees)

New employee users will use the credentials created by the admin to log in with limited permissions (book management only).
____________________________________________________________________

Database and Files
--------------------------------------------------------------------
All data is stored in ebookstore.db (SQLite format).

Book reports are saved in inventory_report.txt in the current directory.

This app is ideal for demonstrating:

Practical use of Python and SQL

Data persistence with SQLite

Role-based access control

Secure password handling

Real-world application structure