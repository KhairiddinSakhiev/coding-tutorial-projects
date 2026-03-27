from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

env = load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL, echo=True)


sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()
    