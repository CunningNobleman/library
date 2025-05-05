from fastapi import FastAPI
from app.routers import books, users, reviews, loans, bookranking

app = FastAPI(
    swagger_ui_parameters={
        "oauth2RedirectUrl": None,
        "displayRequestDuration": True
    }
)

app.include_router(users.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(loans.router)
app.include_router(bookranking.router)

@app.on_event("startup")
def startup():
    pass