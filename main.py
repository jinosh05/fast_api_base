from fastapi import FastAPI, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base, User
from app.schema import UserCreate, UserRead
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
        db_user = User(name=user.name, email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse(content={"status": "ok"})
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
