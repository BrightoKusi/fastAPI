from multiprocessing import synchronize
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




@app.get("/")
def root():
    return {"message": "Hello World"}



#get all posts
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



#create posts
@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#retrieve specified posts
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)): 
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

    return post




#delete posts
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # Query the post
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first()
    
    # Check if the post exists
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
    # Delete the post if it exists
    db.delete(post_to_delete)
    db.commit()
 
    return Response(status_code=status.HTTP_204_NO_CONTENT)




#update posts
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)

    if not post_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # Use post.dict() to dynamically update all columns based on the input
    post_to_update.update(post.dict(), synchronize_session=False)
    
    db.commit()

    return post_to_update.first()


#create users
@app.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session= Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#retrieve specified user
@app.get("/users/{user_name}", response_model=schemas.UserResponse)
def get_user(user_name: str, response: Response, db: Session = Depends(get_db)): 
    user = db.query(models.User).filter(models.User.user_name == user_name).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with user_name: {user_name} not found")

    return user



# uvicorn app.main:app --reload   