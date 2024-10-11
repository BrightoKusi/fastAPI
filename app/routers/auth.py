from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database
from .. import models, schemas, utils
from . import oath2

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def user_login(user_credentials:OAuth2PasswordRequestForm=Depends() , db: Session= Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oath2.create_access_token(data = {"user_id":user.id})

    return {"access_token": access_token, "token_type": "bearer"}


