from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship
from sqlalchemy import func
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Table)

Base = declarative_base()

class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))

    @hybrid_property
    def _id(self):
        """
        Eve backward compatibility
        """
        return self.id

    def jsonify(self):
        """
        Used to dump related objects to json
        """
        relationships = inspect(self.__class__).relationships.keys()
        mapper = inspect(self)
        attrs = [a.key for a in mapper.attrs if \
                a.key not in relationships \
                and not a.key in mapper.expired_attributes]
        attrs += [a.__name__ for a in inspect(self.__class__).all_orm_descriptors if a.extension_type is hybrid.HYBRID_PROPERTY]
        return dict([(c, getattr(self, c, None)) for c in attrs])

powerups = Table('powerups',
                 Base.metadata,
                 Column('character_id', Integer, ForeignKey('character.id')),
                 Column('powerup_id', Integer, ForeignKey('powerup.id'))
)

class Character(CommonColumns):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True)
    description = Column(String)
    powerups = relationship('Powerup',
                            secondary=powerups,
                            backref='character')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Character %r>" % self.name

    def __unicode__(self):
        return self.name

    @classmethod
    def from_tuple(cls, data):
        """ Helper method to populate the database """
        return cls(name=data[0], description=data[1])

class Powerup(CommonColumns):
    __tablename__ = 'powerup'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Powerup %s>" % self.name
