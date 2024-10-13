from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oath2
from ..database import db_engine, get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/posts", tags=['Posts'])


# Get all posts with pagination, filtering, and search
@router.get("/", response_model=List[schemas.VoteResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, first_name: Optional[str] = None, search: Optional[str] = ""):
    # Validate limit
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit must be between 1 and 100")
    
    # Query posts with a count of votes, join with User to allow filtering by first_name
    query = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).join(
        models.User, models.Post.user_id == models.User.id).group_by(models.Post.id)

    # Filter by first_name if provided
    if first_name:
        query = query.filter(models.User.first_name == first_name)

    # Filter by search term in post title
    if search:
        query = query.filter(models.Post.title.contains(search))
    
    # Apply limit for pagination
    posts = query.limit(limit).all()

    # Return the posts in the format expected by VoteResponse schema
    return [{"Post": post, "votes": votes} for post, votes in posts]




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
@router.get("/{id}", response_model=schemas.VoteResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oath2.get_current_user)): 
    
    query = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).join(
        models.User, models.Post.user_id == models.User.id).group_by(models.Post.id)
    
    post = query.filter(models.Post.id == id).first()

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


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oath2.get_current_user)):

    # Fetch the post using .first() to get the actual post object
    post_to_update = db.query(models.Post).filter(models.Post.id == id).first()

    # Check if the post exists
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # Ensure the current user is the owner of the post
    if post_to_update.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to update this post")

    # Update the post with the new data
    for key, value in post.dict().items():
        setattr(post_to_update, key, value)

    # Commit the changes
    db.commit()

    # Refresh the updated post to reflect the changes
    db.refresh(post_to_update)

    return post_to_update
