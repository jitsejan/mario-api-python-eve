from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import func
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime)

Base = declarative_base()

class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))


class Characters(CommonColumns):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80))
    description = Column(String)
    
    @classmethod
    def from_tuple(cls, data):
        """ Helper method to populate the database """
        return cls(name=data[0], description=data[1])


class Worlds(CommonColumns):
    __tablename__ = 'worlds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    world = Column(String(10))
    name = Column(String(120))

    @classmethod
    def from_tuple(cls, data):
        """ Helper method to populate the database """
        return cls(world=data[0], name=data[1])
