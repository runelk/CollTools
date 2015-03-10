from sqlalchemy import Column, Integer, String
from webapp.database import Base


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    document = Column(String(120))
    form = Column(String(120))
    postag = Column(String(120))
    freq = Column(Integer)


class Relation(Base):
    __tablename__ = 'relations'
    id = Column(Integer, primary_key=True)
    document = Column(String(180))
    form1 = Column(String(180))
    postag1 = Column(String(180))
    rel = Column(String(180))
    form2 = Column(String(180))
    postag2 = Column(String(180))
    freq = Column(Integer)
