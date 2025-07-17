import sqlite3

def create_database():
    """
    Creates the SQLite database and required tables if they don't exist.
    Also inserts an initial admin user and default book records.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    # Create book table to store book information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            qty INTEGER
        )
    ''')

    # Create users table to store login credentials
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    # Check if admin user exists, if not create it
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users(username, password) VALUES (?, ?)', ('admin', 'adm1n'))
        print("✅ Admin account created: username = admin, password = adm1n")

    # Insert initial sample books if they do not already exist
    initial_books = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]

    cursor.executemany(
        'INSERT OR IGNORE INTO book(id, title, author, qty) VALUES (?, ?, ?, ?)',
        initial_books
    )

    connection.commit()
    connection.close()


def login_user():
    """
    Prompts the user to enter username and password and verifies them against the database.
    
    Returns:
        username (str): The logged-in username if successful.
        None: If login fails.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    print("🔐 Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    connection.close()

    if user:
        print(f"✅ Welcome, {username}!")
        return username
    else:
        print("❌ Invalid credentials.")
        return None


def display_low_stock_books():
    """
    Queries the database for books with quantity less than 5 and displays them.
    If none are low stock, displays an all-stocked message.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM book WHERE qty < 5')
    low_stock_books = cursor.fetchall()
    connection.close()

    if low_stock_books:
        print("\n⚠️ LOW STOCK BOOKS (Qty < 5):")
        for book in low_stock_books:
            print(f"📘 ID: {book[0]} | Title: {book[1]} | Qty: {book[3]}")
    else:
        print("\n📦 All books are well-stocked (Qty ≥ 5).")


def export_inventory_report():
    """
    Generates and saves a text report of all books sorted by quantity (ascending).
    The report is saved as 'inventory_report.txt'.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM book ORDER BY qty ASC')
    books = cursor.fetchall()
    connection.close()

    with open('inventory_report.txt', 'w', encoding='utf-8') as file:
        file.write("📚 Bookstore Inventory Report\n")
        file.write("=" * 35 + "\n")
        for book in books:
            file.write(
                f"ID: {book[0]}\n"
                f"Title: {book[1]}\n"
                f"Author: {book[2]}\n"
                f"Quantity: {book[3]}\n"
                f"{'-'*35}\n"
            )

    print("✅ Inventory report exported as 'inventory_report.txt'.")


def add_user_account():
    """
    Allows the admin user to add a new user to the users table.
    Prompts for username and password, checks for duplicates.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    username = input("Enter new username: ").strip()
    password = input("Enter password: ").strip()

    try:
        cursor.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
        connection.commit()
        print("✅ User added successfully.")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
    finally:
        connection.close()


def reset_user_password():
    """
    Allows the admin user to reset the password of an existing user.
    Prompts for username and new password.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    username = input("Enter username to reset: ").strip()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

    if cursor.fetchone():
        new_pw = input("Enter new password: ").strip()
        cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_pw, username))
        connection.commit()
        print("✅ Password reset successfully.")
    else:
        print("❌ User not found.")
    connection.close()


def add_book_to_inventory():
    """
    Prompts the user to enter details of a new book and inserts it into the book table.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    try:
        book_id = int(input("Enter book ID: "))
        title = input("Enter title: ")
        author = input("Enter author: ")
        qty = int(input("Enter quantity: "))

        cursor.execute(
            'INSERT INTO book(id, title, author, qty) VALUES (?, ?, ?, ?)',
            (book_id, title, author, qty)
        )

        connection.commit()
        print("✅ Book added successfully.")
    except ValueError:
        print("❌ Invalid input. Book ID and quantity must be integers.")
    except sqlite3.IntegrityError:
        print("❌ Book ID already exists.")
    finally:
        connection.close()


def update_book_details():
    """
    Allows the user to update the title, author, or quantity of an existing book.
    Prompts the user to choose which attribute to update.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    try:
        book_id = int(input("Enter ID of the book to update: "))
    except ValueError:
        print("❌ Invalid book ID.")
        connection.close()
        return

    print("Update:\n1. Title\n2. Author\n3. Quantity")
    choice = input("Choice: ")

    if choice == "1":
        new_value = input("New title: ")
        cursor.execute('UPDATE book SET title = ? WHERE id = ?', (new_value, book_id))
    elif choice == "2":
        new_value = input("New author: ")
        cursor.execute('UPDATE book SET author = ? WHERE id = ?', (new_value, book_id))
    elif choice == "3":
        try:
            new_value = int(input("New quantity: "))
        except ValueError:
            print("❌ Quantity must be an integer.")
            connection.close()
            return
        cursor.execute('UPDATE book SET qty = ? WHERE id = ?', (new_value, book_id))
    else:
        print("❌ Invalid choice.")
        connection.close()
        return

    connection.commit()
    connection.close()
    print("✅ Book updated.")


def delete_book_by_id():
    """
    Deletes a book from the database based on the book ID provided by the user.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    try:
        book_id = int(input("Enter ID of the book to delete: "))
    except ValueError:
        print("❌ Invalid book ID.")
        connection.close()
        return

    cursor.execute('DELETE FROM book WHERE id = ?', (book_id,))

    if cursor.rowcount == 0:
        print("❌ Book not found.")
    else:
        connection.commit()
        print("✅ Book deleted.")
    connection.close()


def search_books_by_id_or_title():
    """
    Allows the user to search for books by either ID or title keyword.
    Displays matching books with their details.
    """
    connection = sqlite3.connect('ebookstore.db')
    cursor = connection.cursor()

    print("Search by:\n1. ID\n2. Title")
    choice = input("Choice: ")

    if choice == "1":
        try:
            book_id = int(input("Enter book ID: "))
        except ValueError:
            print("❌ Invalid book ID.")
            connection.close()
            return
        cursor.execute('SELECT * FROM book WHERE id = ?', (book_id,))
    elif choice == "2":
        title = input("Enter title keyword: ").strip()
        cursor.execute('SELECT * FROM book WHERE LOWER(title) LIKE LOWER(?)', ('%' + title + '%',))
    else:
        print("❌ Invalid choice.")
        connection.close()
        return

    books = cursor.fetchall()

    if books:
        for book in books:
            print(f"📚 ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Qty: {book[3]}")
    else:
        print("❌ No books found.")

    connection.close()


def main():
    """
    Main program loop. Handles user login and displays the menu with options.
    Only admin users have access to user management features.
    """
    create_database()

    user = None
    while not user:
        user = login_user()

    if user:
        display_low_stock_books()

    while True:
        print("\n📘 Bookstore Menu")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. Export inventory report")
        if user == "admin":
            print("6. Add new user")
            print("7. Reset user password")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book_to_inventory()
        elif choice == "2":
            update_book_details()
        elif choice == "3":
            delete_book_by_id()
        elif choice == "4":
            search_books_by_id_or_title()
        elif choice == "5":
            export_inventory_report()
        elif choice == "6" and user == "admin":
            add_user_account()
        elif choice == "7" and user == "admin":
            reset_user_password()
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()
