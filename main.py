from app.core.exceptions import validation_exception_handler, http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.api.v1 import auth, user, console, buffet, unitPrice
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI

app = FastAPI(title="CafeGame", description="API for managing CafeGame", version="1.0.0", responses={
    422: {
        "description": "Validation Error Example",
        "content": {
            "application/json": {
                "example": {
                    "errors": [
                        {"field": "نام فیلد", "message": "متن خطا"}
                    ]
                }
            }
        }
    },
    409: {
        "description": "The resource already exists or violates a unique constraint",
        "content": {
            "application/json": {
                "example": {
                    "error": [
                        {"field": "نام فیلد", "message": "متن خطا"}
                    ]
                }
            }
        }
    },
    401: {
        "description": "The request requires authentication or the provided credentials are invalid",
        "content": {
            "application/json": {
                "example": {
                    "error": {"message": "متن خطا"}
                }
            }
        }
    },
    404: {
        "description": "The requested resource was not found on the server",
        "content": {
            "application/json": {
                "example": {
                    "error": {"message": "متن خطا"}
                }
            }
        }
    }
})

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(console.router)
app.include_router(buffet.router)
app.include_router(unitPrice.router)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
