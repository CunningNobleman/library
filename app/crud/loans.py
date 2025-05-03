from datetime import datetime, timedelta
from ..database import get_db_connection

#get loan by id
def get_loan(loan_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_loans WHERE loan_id = ?', (loan_id,))
    loan = cursor.fetchone()
    conn.close()
    return dict(loan) if loan else None

#select all user's loans
def get_user_loans(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bl.*, b.title, b.author
        FROM book_loans bl
        JOIN books b ON bl.book_id = b.book_id
        WHERE bl.user_id = ?
        ORDER BY bl.due_date ASC
    ''', (user_id,))
    loans = cursor.fetchall()
    conn.close()
    return [dict(loan) for loan in loans]

# add new loan
def create_loan(loan_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    due_date = datetime.now() + timedelta(days=14) #due date is two weeks from borrowing date
    
    cursor.execute(
        '''INSERT INTO book_loans 
           (book_id, user_id, due_date) 
           VALUES (?, ?, ?)''',
        (loan_data['book_id'], 
         loan_data['user_id'],
         due_date))
    
    conn.commit()
    loan_id = cursor.lastrowid
    cursor.execute('SELECT * FROM book_loans WHERE loan_id = ?', (loan_id,))
    new_loan = dict(cursor.fetchone())
    conn.close()
    return new_loan

#updating loan
def return_loan(loan_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE book_loans SET return_date = ? WHERE loan_id = ?',
        (datetime.now(), loan_id)
    )
    conn.commit()
    
    cursor.execute('SELECT * FROM book_loans WHERE loan_id = ?', (loan_id,))
    updated_loan = dict(cursor.fetchone())
    conn.close()
    return updated_loan


# Update book loan
def update_loan(loan_id: int, loan_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        set_clause = ", ".join(f"{key} = ?" for key in loan_data.keys())
        values = list(loan_data.values())
        values.append(loan_id)
        
        cursor.execute(
            f"UPDATE book_loans SET {set_clause} WHERE loan_id = ?",
            values
        )
        conn.commit()
        return get_loan(loan_id)
    finally:
        conn.close()

#delete book loan
def delete_loan(loan_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM book_loans WHERE loan_id = ?", (loan_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()