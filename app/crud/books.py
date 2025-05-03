from ..database import get_db_connection

# Get book by id
def get_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return dict(book) if book else None

# Select number of books
def get_books(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books LIMIT ? OFFSET ?', (limit, skip))
    books = cursor.fetchall()
    conn.close()
    return [dict(book) for book in books]

# Add new book
def create_book(book_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
        (book_data['title'], book_data['author'], book_data['year'])
    )
    conn.commit()
    book_id = cursor.lastrowid
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    new_book = dict(cursor.fetchone())
    conn.close()
    return new_book