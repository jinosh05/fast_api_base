from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 422:
        return JSONResponse(
            status_code=200,
            content={"status": "NOT_OK", "message": "Invalid Username"},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        if error["loc"] == ("body", "name"):
            return JSONResponse(
                status_code=200,
                content={"status": "NOT_OK", "message": "Invalid Username"},
            )
    return JSONResponse(
        status_code=400,
        content={"status": "NOT_OK", "message": "Validation Error", "detail": exc.errors()},
    )