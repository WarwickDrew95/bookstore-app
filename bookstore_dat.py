import sqlite3

def create_db():
    """
    Creates the database and its tables if they don't exist.
    Also inserts initial admin user and default books.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            qty INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users(username, password) VALUES (?, ?)', (
            'admin', 'adm1n'))
        print("✅ Admin account created: username = admin, password = adm1n")

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

    db.commit()
    db.close()


def login():
    """
    Prompts the user to log in and verifies credentials.
    Returns the username if successful, else None.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    print("🔐 Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    )
    user = cursor.fetchone()
    db.close()

    if user:
        print(f"✅ Welcome, {username}!")
        return username
    else:
        print("❌ Invalid credentials.")
        return None


def display_low_stock_books():
    """
    Displays books with quantity less than 5.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM book WHERE qty < 5')
    low_stock = cursor.fetchall()
    db.close()

    if low_stock:
        print("\n⚠️ LOW STOCK BOOKS (Qty < 5):")
        for book in low_stock:
            print(f"📘 ID: {book[0]} | Title: {book[1]} | Qty: {book[3]}")
    else:
        print("\n📦 All books are well-stocked (Qty ≥ 5).")


def export_inventory_report():
    """
    Exports the book inventory sorted by quantity to a text file.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    cursor.execute('SELECT * FROM book ORDER BY qty ASC')
    books = cursor.fetchall()
    db.close()

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


def add_user():
    """
    Allows admin to create a new employee login.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    username = input("Enter new username: ").strip()
    password = input("Enter password: ").strip()

    try:
        cursor.execute(
            'INSERT INTO users(username, password) VALUES (?, ?)',
            (username, password)
        )
        db.commit()
        print("✅ User added successfully.")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
    finally:
        db.close()


def reset_password():
    """
    Allows admin to reset a user's password.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    username = input("Enter username to reset: ").strip()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

    if cursor.fetchone():
        new_pw = input("Enter new password: ").strip()
        cursor.execute(
            'UPDATE users SET password = ? WHERE username = ?',
            (new_pw, username)
        )
        db.commit()
        print("✅ Password reset successfully.")
    else:
        print("❌ User not found.")
    db.close()


def enter_book():
    """
    Allows the user to enter a new book into the database.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    book_id = int(input("Enter book ID: "))
    title = input("Enter title: ")
    author = input("Enter author: ")
    qty = int(input("Enter quantity: "))

    cursor.execute(
        'INSERT INTO book(id, title, author, qty) VALUES (?, ?, ?, ?)',
        (book_id, title, author, qty)
    )

    db.commit()
    db.close()
    print("✅ Book added successfully.")


def update_book():
    """
    Allows the user to update an existing book's info.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    book_id = int(input("Enter ID of the book to update: "))
    print("Update:\n1. Title\n2. Author\n3. Quantity")
    choice = input("Choice: ")

    if choice == "1":
        new = input("New title: ")
        cursor.execute('UPDATE book SET title = ? WHERE id = ?', (new, book_id))
    elif choice == "2":
        new = input("New author: ")
        cursor.execute('UPDATE book SET author = ? WHERE id = ?', (new, book_id))
    elif choice == "3":
        new = int(input("New quantity: "))
        cursor.execute('UPDATE book SET qty = ? WHERE id = ?', (new, book_id))
    else:
        print("❌ Invalid choice.")
        db.close()
        return

    db.commit()
    db.close()
    print("✅ Book updated.")


def delete_book():
    """
    Deletes a book from the database by ID.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    book_id = int(input("Enter ID of the book to delete: "))
    cursor.execute('DELETE FROM book WHERE id = ?', (book_id,))

    if cursor.rowcount == 0:
        print("❌ Book not found.")
    else:
        db.commit()
        print("✅ Book deleted.")
    db.close()


def search_books():
    """
    Searches for books by ID or title keyword (case-insensitive).
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    print("Search by:\n1. ID\n2. Title")
    choice = input("Choice: ")

    if choice == "1":
        book_id = int(input("Enter book ID: "))
        cursor.execute('SELECT * FROM book WHERE id = ?', (book_id,))
    elif choice == "2":
        title = input("Enter title keyword: ").strip()
        cursor.execute(
            'SELECT * FROM book WHERE LOWER(title) LIKE LOWER(?)',
            ('%' + title + '%',)
        )
    else:
        print("❌ Invalid choice.")
        db.close()
        return

    books = cursor.fetchall()

    if books:
        for book in books:
            print(
                f"📚 ID: {book[0]} | Title: {book[1]} | "
                f"Author: {book[2]} | Qty: {book[3]}"
            )
    else:
        print("❌ No books found.")

    db.close()


def main():
    """
    Main function that controls user login and menu.
    """
    create_db()

    user = None
    while not user:
        user = login()

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
            enter_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_books()
        elif choice == "5":
            export_inventory_report()
        elif choice == "6" and user == "admin":
            add_user()
        elif choice == "7" and user == "admin":
            reset_password()
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()
