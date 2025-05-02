from fastapi import FastAPI
from .database import engine, Base
from .routers import books, users, reviews, loans

app = FastAPI()

# All routes
app.include_router(users.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(loans.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)