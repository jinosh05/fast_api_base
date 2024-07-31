from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import app


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# @app.post("/users/", response_model=UserCreate)
# async def create_user(user: UserCreate):
#     try:
#         # Here you would normally save the user to the database
#         # For the sake of this example, we just return the user
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

