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

import json
import socket
import base64
from datetime import datetime
import time
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
def currdir(filename):
  return os.path.join(os.path.dirname(__file__), filename)

def loadUserConfig(filename=currdir( "userconfig.json")):
  with open(filename, 'r') as myfile:
    toparse = myfile.read()

  a = json.loads(toparse)
  if not(a.has_key('username') and a.has_key('password')) or\
      not(a['username'] and a['password']):
    print "Please provide a username and a password in the config file userconfing.json"
    exit()
  return a


def connectuser(user, sock):
  # authentificate
  sock.send('auth %s %s' % (user['user'], user['pass']))
  if sock.recv(3) == 'SUC' :
    token = sock.recv(64)
    user['token'] = token
  else :
    sock.close()
    print 'Could not connect'
    exit(0)
  return user

class Client(object):

  def __init__(self, sock, user, token):
    self.sock = sock
    self.user = user
    self.token = token

  def listall(self):
    self.sock.send('lsall %s %s\n' % (self.user, self.token))
    data = self.sock.recv(4096)
    # I think this can cause security issue
    return eval(base64.b64decode(data))

  def ls(self):
    self.sock.send('ls %s %s\n' % (self.user, self.token))
    data= self.sock.recv(4096)
    return eval(base64.b64decode(data))

  def add(self, todotext):
    self.sock.send('add %s %s %s' % (self.user, self.token, todotext))


  def done(self, num):
    self.sock.send('done %s %s %s' % (self.user, self.token, num))

  def undone(self, num):
    self.sock.send('undone %s %s %s' % (self.user, self.token, num))

  def remove(self, num):
    self.sock.send('remove %s %s %s' % (self.user, self.token, num))


def display(out):
  try:
    from colorama import init, Fore
  except ImportError:
    # Well that's my ugly hack
    class Fore:
      YELLOW = ''
      RESET  = ''
      GREEN  = ''
      RED    = ''
  else : init()
  try:
    TICK = u'\u2713'.encode(sys.stdout.encoding, errors='strict')
    ERROR = Fore.RED+u'\u2718'.encode(sys.stdout.encoding, errors='strict')
  except UnicodeEncodeError : 
    ERROR = 'Not Yet'
    TICK = 'Done'
  for i, row in enumerate(out):
    parsed = time.strptime(row[4], "%Y/%m/%d %H:%M:%S")

    d = (datetime.today() - datetime(parsed.tm_year, parsed.tm_mon, parsed.tm_mday)).days
    dayz = str(d)+' days ago' if d else 'today'
    print u'%i) %s, %s %s' % (i, row[2].encode('utf-8'), Fore.YELLOW+dayz+Fore.RESET,
                            Fore.GREEN+TICK+Fore.RESET \
                          if row[3] else Fore.RED+ERROR+Fore.RESET)

def initall():

  a = loadUserConfig()
  user = {
    'user' : a['username'],
    'pass' : a['password'],
    'token': ''
  }
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_adress = (a['host'][0], a['host'][1])
  sock.connect(server_adress)
  return user, sock

