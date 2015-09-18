

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from . import app
import time

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base()

Session = sessionmaker(bind=engine)

class Todo(Base):
  __tablename__ = 'Todo'
  id = Column(Integer, primary_key=True)
  owner = Column(Integer)
  todotext = Column(String)
  done = Column(Integer)
  date = Column(String)

  def __init__(self, ow, tt):
    self.owner = ow
    self.todotext = tt
    self.done = 0
    self.date = time.strftime('%Y/%m/%d %H:%M:%S')

  def __str__(self):
    return "(%d, %d, %s, %d, %s)" % (self.id,
                                     self.owner,
                                     self.todotext,
                                     self.done,
                                     self.date)

class User(Base):
  __tablename__ = 'Users'
  id = Column(Integer, primary_key=True)
  username = Column(String)
  password = Column(String)

