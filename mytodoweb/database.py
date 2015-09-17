

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:////home/mohamed/myFiles/mytodo/todo.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)

class Todo(Base):
  __tablename__ = 'Todo'
  id = Column(Integer, primary_key=True)
  owner = Column(Integer)
  todotext = Column(String)
  done = Column(Integer)
  date = Column(String)

  def __str__(self):
    return "(%d, %d, %s, %d, %s)" % (self.id,
                                     self.owner,
                                     self.todotext,
                                     self.done,
                                     self.date)

