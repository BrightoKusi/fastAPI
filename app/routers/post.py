from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from typing import List
from .. import models, schemas, oath2
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
def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db), current_user: schemas.TokenData = Depends(oath2.get_current_user)):
    print(f"Current user ID: {current_user.id}")
    new_post = models.Post(**post.dict(), user_id=current_user.id)
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





# delete posts
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: schemas.TokenData = Depends(oath2.get_current_user)):
    # Query the post
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first()
    print(current_user.id)
    print(post_to_delete.user_id)
    print(f"Current user ID: {current_user.id} (type: {type(current_user.id)})")
    print(f"Post user ID: {post_to_delete.user_id} (type: {type(post_to_delete.user_id)})")

    # Check if the post exists
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    # Ensure the current user is the owner of the post
    if post_to_delete.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to delete this post")

    
    # Delete the post if it exists and the user is authorized
    db.delete(post_to_delete)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update posts
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
                , current_user: schemas.TokenData = Depends(oath2.get_current_user)):
    
    post_to_update = db.query(models.Post).filter(models.Post.id == id).first()

    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # Ensure the current user is the owner of the post
    if post_to_update.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to delete this post")

    # Use post.dict() to dynamically update all columns based on the input
    post_to_update.update(post_to_update.dict(), synchronize_session=False)
    
    db.commit()

    return post_to_update
