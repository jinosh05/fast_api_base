from sqlalchemy import Integer, String , Column
from app.database import Base

class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True, index=True) 