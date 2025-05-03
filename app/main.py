from fastapi import FastAPI
from app.routers import books, users, reviews, loans

app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(loans.router)

@app.on_event("startup")
def startup():
    # Database is initialized automatically via database.py
    pass