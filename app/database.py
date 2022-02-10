from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:kehinde@127.0.0.1:5433/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@' \
                          f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# If not using SQLALCHEMY and connecting to Postgres
while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', port=5433, user='postgres', password='kehinde',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successfull.......")
        break
    except Exception as error:
        print("Connection to Database failed")
        print("Error: ", error)
        time.sleep(2)
