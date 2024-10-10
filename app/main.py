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
    rating: Optional[int] = None

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
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    print(posts)

    return posts


#create posts
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cur.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
                (post.title, post.content, post.published))
    new_post = cur.fetchone()
    conn.commit()

    return new_post


#retrieve specified posts
@app.get("/posts/{id}")
def get_post(id: int, response: Response): 
    cur.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)),)
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return {"post detail": post}


#delete posts
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cur.fetchone()
    conn.commit() 

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update posts
@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    
    cur.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
                (post.title, post.content,post.published, str(id)))
    updated_post = cur.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")   

    return updated_post


# uvicorn app.main:app --reload   