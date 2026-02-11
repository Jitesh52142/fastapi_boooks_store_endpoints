from fastapi import FastAPI
from app.api.v1.routes import user_routes, book_routes, cart_routes, order_routes, review_routes

app = FastAPI(
    title="Online Bookstore API",
    description="Complete REST API for Online Bookstore",
    version="1.0.0"
)

app.include_router(user_routes.router)
app.include_router(book_routes.router)
app.include_router(cart_routes.router)
app.include_router(order_routes.router)
app.include_router(review_routes.router)
