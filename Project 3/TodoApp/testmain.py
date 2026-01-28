from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
import models
from database import SessionLocal, engine
# from routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
# Scan all my model classes and make sure their tables exist in the connected database.
# In a FastAPI app, you usually define your database models using SQLAlchemy’s ORM (Object Relational Mapper).
# Here, Base is a SQLAlchemy declarative base — it keeps track of all the models you define by inheriting from it.
# Base.metadata is a container that holds all the database schema information for the models derived from that Base (like User, Post, etc.).
# create_all(bind=engine):  Look at all the models I’ve defined, and create those tables in the database if they don’t already exist.
# Scan all my model classes and make sure their tables exist in the connected database.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    #Depends is dependency injection which tells FastAPI to execute the get_db function and provide the resulting database session as an argument to the read_all function.
    return db.query(models.User).all()

# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)