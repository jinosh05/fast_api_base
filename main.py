from fastapi import FastAPI, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import *
from app.models import *
from app.schema import *
from sqlalchemy.exc import IntegrityError

# Import the custom exception handler
from app.exceptions import validation_exception_handler


app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

# Register the custom exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)


@app.get('/')
def get_home():
    return { "status":"OK", "message": "Welcome to Home Page"}

@app.get('/users/')
def get_all_users(db: Session=Depends(get_db)):
    try:
       users = db.query(User).all()
       user_responses = [UserRead.from_orm(user) for user in users]
       return JSONResponse(
            content={
                "users": [user.dict() for user in user_responses]
            }
        )
    except Exception as e:
         db.rollback()
         raise HTTPException(status_code=400,detail=f"Error: {str(e)}")

@app.post('/users/')
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
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

