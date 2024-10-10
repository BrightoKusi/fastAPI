from sqlalchemy import TEXT, TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.sql import text
from .database import BASE

class Post(BASE):   
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text("true"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('NOW()'))

# alembic revision --autogenerate -m "CREATED_AT timestamp column"
# alembic revision --autogenerate -m "Your migration message"
