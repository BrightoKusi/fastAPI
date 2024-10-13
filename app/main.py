from fastapi import FastAPI
from . import models
from .database import db_engine
from .routers import post, user, auth, vote
from .config import settings
#
app = FastAPI()

models.BASE.metadata.create_all(bind=db_engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}




# uvicorn app.main:app --reload   