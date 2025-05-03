from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .models import TokenData
from .crud.users import get_user
from .database import get_db_connection

SECRET_KEY = "ba32c1bf6f5c1e9211992a687556b7038d0fa07fbf2b55180d2e09ddf25797c0b265f58081e206927c7c7a813ab522eafe3068e647059bf0774db9764523c5c988417d25cf6f6fae5a5cb7bc95b28dd212d03bafa7ca5a8741a66047cc471a883f4b36d1d63c3889945549e9ea66b673fe98c733b30b7ca3cbd4ac82f013470f"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    db = get_db_connection()
    try:
        user = get_user(db, username=token_data.username)
        return user
    finally:
        db.close()
    
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt