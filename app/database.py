from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_engine = create_engine("postgresql://postgres:260695@localhost:5432/fastapi")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

BASE = declarative_base()

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
