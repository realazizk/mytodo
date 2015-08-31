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

def loadUserConfig(filename="userconfig.json"):
  with open(filename, 'r') as myfile:
    toparse = myfile.read()

  a = json.loads(toparse)
  if not(a.has_key('username') and a.has_key('password')) or\
      not(a['username'] and a['password']):
    print "Please provide a username and a password in the config file userconfing.json"
    exit()
  return a


a = loadUserConfig()

user = {
  'user' : a['username'],
  'pass' : a['password'],
  'token': ''
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_adress = (a['host'][0], a['host'][1])
sock.connect(server_adress)

def connectuser(user):
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

def listall(user, token):
  sock.send('lsall %s %s' % (user, token))
  data = sock.recv(4096)
  # I think this can cause security issue
  return eval(base64.b64decode(data))

def ls(user, token):
  sock.send('ls %s %s' % (user, token))
  data= sock.recv(4096)
  return eval(base64.b64decode(data))

def add(todotext, user, token):
  sock.send('add %s %s %s' % (user, token, todotext))

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

  for i, row in enumerate(out):
    parsed = time.strptime(row[4], "%Y/%m/%d %H:%M:%S")

    d = (datetime.today() - datetime(parsed.tm_year, parsed.tm_mon, parsed.tm_mday)).days
    dayz = str(d)+' days ago' if d else 'today'
    print u'%i) %s, %s %s' % (i, row[2], Fore.YELLOW+dayz+Fore.RESET,
                             Fore.GREEN+u'\u2713'+Fore.RESET \
                          if row[3] else Fore.RED+u'\u2718'+Fore.RESET)

def done(num, user, token):
  sock.send('done %s %s %s' % (user, token, num))

def undone(num, user, token ):
  sock.send('undone %s %s %s' % (user, token, num))

def remove(num, user, token):
  sock.send('remove %s %s %s' % (user, token, num))


