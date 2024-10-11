from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, utils
from ..database import db_engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=['Users'])


#create users
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session= Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



#retrieve specified user
@router.get("/{username}", response_model=schemas.UserResponse)
def get_user(username: str, response: Response, db: Session = Depends(get_db)): 
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with user_name: {username} not found")

    return user



