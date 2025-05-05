'''routers for users table operations'''
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..models import User, UserCreate, Token, UserUpdate
from ..crud.users import get_user, create_user, authenticate_user, update_user, delete_user
from ..dependencies import create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user_route(user: UserCreate):
    '''creating a new user'''
    db_user = get_user(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(user.dict())

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    '''getting a token'''
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user['username']},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/{username}", response_model=User)
def update_user_route(
    username: str,
    user_update: UserUpdate,
):
    '''updating a user entry'''
    db_user = get_user(username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    updated_user = update_user(username, update_data)

    if not updated_user:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    return updated_user

@router.delete("/{username}")
def delete_user_route(username: str):
    '''deleting an entry'''
    if not get_user(username):
        raise HTTPException(status_code=404, detail="User not found")
    if not delete_user(username):
        raise HTTPException(status_code=400, detail="Delete failed")
    return {"message": "User deleted successfully"}
