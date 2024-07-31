from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import *
from app.models import *
from app.schema import *
from sqlalchemy.exc import IntegrityError
from typing import List

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

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
async def create_user(user: UserCreate,db:Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password=user.password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"Error: {str(e)}" )
    
    return db_user
