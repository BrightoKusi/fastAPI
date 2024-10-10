from multiprocessing import synchronize
from random import randrange
from time import sleep
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import db_engine, get_db
from sqlalchemy.orm import Session



app = FastAPI()

models.BASE.metadata.create_all(bind=db_engine)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 





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




my_posts = [{"title": "title of post 1", "content":"content of post 1", "id": 1}
            , {"title": "favorite animes", "content":"I like black clover", "id": 2}
            ]

def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:  
            return post
    return None  

def find_index_of_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None



@app.get("/")
def root():
    return {"message": "Hello World"}

#testing ORM
@app.get("/sqlalchemy")
def test_post(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts





#get all posts
@app.get("/posts")
def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



#create posts
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session= Depends(get_db)):
    # cur.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
    #             (post.title, post.content, post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#retrieve specified posts
@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session= Depends(get_db)): 
    # cur.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)),)
    # post = cur.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return  post


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
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)

    if not post_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # Use post.dict() to dynamically update all columns based on the input
    post_to_update.update(post.dict(), synchronize_session=False)
    
    db.commit()

    return post_to_update.first()


# uvicorn app.main:app --reload   