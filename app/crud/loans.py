'''crud operatins for loans table'''
from datetime import datetime, timedelta
from ..database import get_db_connection

#get loan by id
def get_loan(loan_id: int):
    '''getting loan by id'''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_loans WHERE loan_id = ?', (loan_id,))
    loan = cursor.fetchone()
    conn.close()
    return dict(loan) if loan else None

#select all user's loans
def get_user_loans(user_id: int):
    '''getting loans by user'''
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
    '''creating a new loan'''
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
def update_loan(loan_id: int, loan_update: dict):
    '''updating a loan entry'''
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        update_data = {}

        if loan_update.get('book_id'):
            update_data['book_id'] = loan_update['book_id']

        if loan_update.get('user_id'):
            update_data['user_id'] = loan_update['user_id']

        if loan_update.get('loan_date'):
            update_data['loan_date'] = loan_update['loan_date']

        if loan_update.get('due_date'):
            update_data['due_date'] = loan_update['due_date']

        if loan_update.get('return_date'):
            update_data['return_date'] = loan_update['return_date']

        if not update_data:
            return None

        set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
        values = list(update_data.values())
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
    '''deleting an entry'''
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM book_loans WHERE loan_id = ?", (loan_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
