from fastapi import FastAPI
from . import models
from .database import db_engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# models.BASE.metadata.create_all(bind=db_engine)



# List of origins that should be allowed to make cross-origin requests
origins = [
    "https://www.google.com"] # React development server


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # Allow only the specified origins
    allow_credentials=True,  # Allow cookies and credentials to be sent
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers to be sent
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}




# uvicorn app.main:app --reload   