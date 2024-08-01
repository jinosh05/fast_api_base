from fastapi import FastAPI, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base, User
from app.schema import *
from sqlalchemy.exc import IntegrityError
from app.exceptions import validation_exception_handler

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

# Register the custom exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)


@app.get('/')
def get_home():
    """
    Home endpoint to check the API status.
    Returns a welcome message.
    """
    return {"status": "OK", "message": "Welcome to Home Page"}


@app.get('/users/')
def get_all_users(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all users.
    Returns a list of users.
    """
    try:
        users = db.query(User).all()
        user_responses = [UserRead.from_orm(user) for user in users]
        return JSONResponse(content={"users": [user.dict() for user in user_responses]})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@app.post('/users/')
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user.
    Accepts user details and returns a success message.
    """
    try:
        db_user = User(name=user.name, email=user.email,
                       password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse(content={"status": "ok"})
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=200,
            content={"status": "NOT_OK",
                     "message": "Email already registered"},
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@app.put('/users/{user_id}')
def update_user_by_id(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update User By ID

    This endpoint allows updating a user's details by their ID.

    Parameters:
    - user_id: int - The ID of the user to update
    - user: UserUpdate - The new details for the user
    - db: Session - The database session (injected by FastAPI's Depends)

    Returns:
    - JSONResponse with status and message
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return JSONResponse(
                status_code=200,
                content={"status": "NOT_OK", "message": "User Not Found"},
            )

        db_user.name = user.name
        db_user.email = user.email
        db_user.password = user.password
        db.commit()

        return JSONResponse(
            status_code=200,
            content={"status": "OK", "message": "User updated successfully"},
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@app.delete("/users/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db), ):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return JSONResponse(
                status_code=200,
                content={"status": "NOT_OK", "message": "User Not Found"},
            )
        db.delete(db_user)
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"status": "OK",
                     "message": "User Account Deleted successfully"},
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
