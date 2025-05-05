'''crud operations for books table'''
from ..database import get_db_connection

# Get book by id
def get_book(book_id: int):
    '''getting book by id'''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return dict(book) if book else None

# Select number of books
def get_books(skip: int = 0, limit: int = 100):
    '''getting number of books'''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books LIMIT ? OFFSET ?', (limit, skip))
    books = cursor.fetchall()
    conn.close()
    return [dict(book) for book in books]

# Add new book
def create_book(book_data: dict):
    '''adding a new book'''
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

#update book
def update_book(book_id: int, book_update: dict):
    '''updating an entry'''
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        update_data = {}
        if book_update.get('title'):
            update_data['title'] = book_update['title']
        
        if book_update.get('author'):
            update_data['author'] = book_update['author']
        
        if book_update.get('year'):
            update_data['year'] = book_update['year']
        
        if not update_data:
            return None
            
        set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
        values = list(update_data.values())
        values.append(book_id)
        
        cursor.execute(
            f"UPDATE books SET {set_clause} WHERE book_id = ?",
            values
        )
        conn.commit()
        return get_book(book_id)
    finally:
        conn.close()

#delete book
def delete_book(book_id: int):
    '''deleting an entry'''
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
