from passlib.context import CryptContext
from ..database import get_db_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Get user by username
def get_user(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

#Add new user to the table
def create_user(user_data: dict):
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
    user = get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user['hashed_password']):
        return False
    return user