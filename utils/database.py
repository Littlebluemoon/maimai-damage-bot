from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

engine = create_engine(f"sqlite:///{os.getenv('DATABASE_PATH')}", echo=True)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()