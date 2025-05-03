from ..database import get_db_connection

#get review by id
def get_review(review_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews WHERE review_id = ?', (review_id,))
    review = cursor.fetchone()
    conn.close()
    return dict(review) if review else None

#get review by book_id
def get_reviews_by_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.*, u.username 
        FROM reviews r
        JOIN users u ON r.user_id = u.user_id
        WHERE r.book_id = ?
        ORDER BY r.created_at DESC
    ''', (book_id,))
    reviews = cursor.fetchall()
    conn.close()
    return [dict(review) for review in reviews]

#Create review
def create_review(review_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    
    cursor.execute('SELECT 1 FROM books WHERE book_id = ?', (review_data['book_id'],))
    if not cursor.fetchone():
        conn.close()
        raise ValueError("Book not found")
    
    cursor.execute(
        '''INSERT INTO reviews 
           (book_id, user_id, rating, comment) 
           VALUES (?, ?, ?, ?)''',
        (review_data['book_id'], 
         review_data['user_id'],
         review_data['rating'],
         review_data.get('comment')))
    
    conn.commit()
    review_id = cursor.lastrowid
    cursor.execute('SELECT * FROM reviews WHERE review_id = ?', (review_id,))
    new_review = dict(cursor.fetchone())
    conn.close()
    return new_review

#delete review
def delete_review(review_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM reviews WHERE review_id = ?", (review_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()