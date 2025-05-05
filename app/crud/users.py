'''crud operations for users table'''
from passlib.context import CryptContext
from ..database import get_db_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Get user by username
def get_user(username: str):
    '''getting user by their username'''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

#Add new user to the table
def create_user(user_data: dict):
    '''creating a new entry'''
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = pwd_context.hash(user_data['password'])
    cursor.execute(
        'INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)',
        (user_data['username'], user_data['email'], hashed_password)
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.execute('SELECT user_id, username, email FROM users WHERE user_id = ?', (user_id,))
    new_user = dict(cursor.fetchone())
    conn.close()
    return new_user


def authenticate_user(username: str, password: str):
    '''authetication'''
    user = get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user['hashed_password']):
        return False
    return user

#update user information
def update_user(username: str, user_update: dict):
    '''updating an entry'''
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        update_data = {}

        if user_update.get('username'):
            update_data['username'] = user_update['username']

        if user_update.get('email'):
            update_data['email'] = user_update['email']

        if user_update.get('password'):
            update_data['hashed_password'] = pwd_context.hash(user_update['password'])

        if not update_data:
            return None

        set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
        values = list(update_data.values())
        values.append(username)

        cursor.execute(
            f"UPDATE users SET {set_clause} WHERE username = ?",
            values
        )
        conn.commit()

        updated_username = update_data.get('username', username)
        return get_user(updated_username)
    finally:
        conn.close()

#delete user
def delete_user(username: str):
    '''deleting an  entry'''
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
