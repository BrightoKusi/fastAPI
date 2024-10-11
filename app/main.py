from random import randrange
from time import sleep
from typing import Optional, List
from fastapi import Body, FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import db_engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth


app = FastAPI()

models.BASE.metadata.create_all(bind=db_engine)


while True:  
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="fastapi",
            user="postgres",
            password="260695",
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        print("Connection successful")
        break  

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        sleep(2) 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}




# uvicorn app.main:app --reload   