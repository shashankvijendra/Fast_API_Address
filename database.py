"""
file : database.py
Description :  db changes
Author : Shashank.V
"""

from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, String, Integer
from coordinates import location_address


class Address(BaseModel):
    address: str
    coordinates: str
    is_true: bool

    class Config:
        orm_mode = True


SQLALCHEMY_DATABASE_URL = 'sqlite:///syn.sqlite3'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DBPlace(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(50))
    coordinates = Column(String, nullable=True)
    is_true = Column(Boolean)

Base.metadata.create_all(bind=engine)


def get_place(db: Session, place_id: int):
    return db.query(DBPlace).where(DBPlace.id == place_id).first()

def get_places(db: Session):
    return db.query(DBPlace).all()

def create_place(db: Session, place: Address):
    db_place = DBPlace(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place
    