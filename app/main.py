from fastapi import FastAPI
from app.routers import books, users, reviews, loans

app = FastAPI()

app.swagger_ui_oauth2_redirect_url = None
app.swagger_ui_init_oauth = None

app.include_router(users.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(loans.router)

@app.on_event("startup")
def startup():
    pass