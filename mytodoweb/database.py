#!/usr/bin/env python2
#Copyright (C) 2015 Mohamed Aziz knani

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

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

