
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, backref

DB_FILENAME = 'sqlite:///test.db'

engine = create_engine(DB_FILENAME, convert_unicode=True, echo=True)
Base = declarative_base()

Base.metadata.reflect(engine)


# class Words(Base):
#     __table__ = Base.metadata.tables['words']


# class Relations(Base):
#     __table__ = Base.metadata.tables['relations']


def db_init():
    Base.metadata.create_all(bind=engine)
