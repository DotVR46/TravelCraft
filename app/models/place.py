from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from app.db.session import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
