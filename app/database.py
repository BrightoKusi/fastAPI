from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep

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



# while True:  
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             dbname="fastapi",
#             user="postgres",
#             password="260695",
#             cursor_factory=RealDictCursor
#         )
#         cur = conn.cursor()
#         print("Connection successful")
#         break  

#     except psycopg2.Error as e:
#         print(f"Error connecting to the database: {e}")
#         sleep(2) 

