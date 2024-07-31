from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import *
from app.models import *
from app.schema import UserCreate
from sqlalchemy.exc import IntegrityError


app = FastAPI()

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)


@app.get('/')
def get_home():
    return { "status":"OK", "message": "Welcome to Home Page"}


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
