from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError
from app.api.v1.routes import user_routes, book_routes, cart_routes, order_routes, review_routes

app = FastAPI(
    title="Online Bookstore API",
    description="Complete REST API for Online Bookstore",
    version="1.0.0"
)

# Include Routers
app.include_router(user_routes.router)
app.include_router(book_routes.router)
app.include_router(cart_routes.router)
app.include_router(order_routes.router)
app.include_router(review_routes.router)


@app.get("/")
async def root():
    return {
        "message": "Online Bookstore API is running",
        "version": "1.0.0"
    }




@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation Error",
            "details": exc.errors()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )


@app.exception_handler(PyMongoError)
async def mongo_exception_handler(request: Request, exc: PyMongoError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Database Error"
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal Server Error"
        }
    )
