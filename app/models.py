from tkinter import CASCADE
from sqlalchemy import TEXT, TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql import text
from .database import BASE
from sqlalchemy.orm import relationship


class Post(BASE):   
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text("true"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
     

     
class User(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)  
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('NOW()'))


class Vote(BASE):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
