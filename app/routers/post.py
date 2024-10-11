from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from typing import List
from .. import models, schemas
from ..database import db_engine, get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/posts", tags=['Posts'])

#get all posts
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



#create posts
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#retrieve specified posts
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)): 
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

    return post




#delete posts
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)

    if not post_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # Use post.dict() to dynamically update all columns based on the input
    post_to_update.update(post.dict(), synchronize_session=False)
    
    db.commit()

    return post_to_update.first()
