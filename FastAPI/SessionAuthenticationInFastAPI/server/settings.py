from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql+psycopg2://postgres:Sakhi2000%40postgres@localhost/test_db"
DATABASE_URL = "sqlite:///test_db.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_connection():
    db = SessionLocal()
    return db

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()