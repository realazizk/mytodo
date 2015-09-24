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

from datetime import datetime
import time
import os
import sys
from urlparse import urljoin
import requests
import json
from os.path import expanduser, join

reload(sys)
sys.setdefaultencoding('utf8')

def currdir(filename):
  return os.path.join(os.path.dirname(__file__), filename)

def loadUserConfig(filename=join(expanduser('~'), 'mytodoconfig.json')):
  with open(filename, 'r') as myfile:
    toparse = myfile.read()
  global a
  a = json.loads(toparse)
  if not(a.has_key('username') and a.has_key('password')) or\
      not(a['username'] and a['password']):
    print "Please provide a username and a password in the config file userconfing.json"
    exit()
  return a

def dictToList(sic):
  a = []
  sic = json.loads(sic)
  for i in range(len(sic)):
    a.append( sic[str(i)].values() )
  return a

class Client(object):

  def __init__(self, user, password):
    self.cord = {
      'username' : user,
      'password' : password
    }

    self.req = requests.post

  def listall(self):
    c = self.req(urljoin(a['host'], '/api/get/?action=all'), data=self.cord).text
    return dictToList(c)

  def ls(self):
    c = self.req(urljoin(a['host'], '/api/get/?action=ls'), data=self.cord).text
    return dictToList(c)

  def add(self, todotext):
    self.cord['text'] = todotext
    self.req(urljoin(a['host'], '/api/set/?action=add'), data=self.cord)

  def done(self, num):
    self.req(urljoin(a['host'], '/api/set/?action=done&index=%s' % str(num)), data=self.cord)

  def undone(self, num):
    self.req(urljoin(a['host'], '/api/set/?action=undone&index=%s' % str(num)), data=self.cord)

  def remove(self, num):
    self.req(urljoin(a['host'], '/api/set/?action=remove&index=%s' % str(num)), data=self.cord)

  def category(self, tag):
    c = self.req(urljoin(a['host'], '/api/get/?action=search&tag=%s' % tag), data=self.cord).text
    return dictToList(c)

def dy (date) :
  parsed = time.strptime(date, "%Y/%m/%d %H:%M:%S")
  d = (datetime.today() - datetime(parsed.tm_year, parsed.tm_mon, parsed.tm_mday)).days
  return str(d)+' days ago' if d else 'today'

