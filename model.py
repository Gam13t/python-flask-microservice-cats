from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base


class Cat(Base):
    __tablename__ = 'cat'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    breed = Column(String(128))
    color = Column(String(50))

    def __init__(self, name=None, breed=None, color=None):
        self.name = name
        self.breed = breed
        self.color = color

    def __repr__(self):
        return '<Cats %r>' % self.name