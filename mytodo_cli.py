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

import socket
import argparse
from sys import argv
import base64
import time
from datetime import datetime

# Here set your user and password
user = {
  'user' : 'mohamed',
  'pass' : 'root',
  'token': ''
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_adress = ('localhost', 7060)
sock.connect(server_adress)
def argument_parser():
  parser = argparse.ArgumentParser(description='mytodo script')
  parser.add_argument('-la', '--listall', help='List all todo\'s', dest='listall', action='store_true')
  parser.add_argument('-l', '--list', help='List undone todo\'s', dest='ls', action='store_true')
  parser.add_argument('-u', help='Set up your username from the database' ,dest='user')
  parser.add_argument('-p', help='Set up your password from the database', dest='passwd')
  parser.add_argument('-a', help='Add a new todo', dest='add')
  parser.add_argument('-d', '--done'  , help='Mark as done', dest='done')
  parser.add_argument('-ud', '--undone'  , help='Mark as undone', dest='undone')
  parser.add_argument('-r', '--remove'  , help='Rmove an entry', dest='remove')
  args = parser.parse_args()
  return (args, args.user or user['user'], args.passwd or user['pass'])

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
  from colorama import init, Fore
  init()
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

if __name__ == '__main__':
  arguments, user['user'], user['pass'] = argument_parser()
  #try:
  user = connectuser(user)
  if arguments.listall:
    out = listall(user['user'], user['token'])
    #print out
    display(out)
  elif arguments.add:
    add(arguments.add, user['user'], user['token'])
  elif arguments.done:
    done(arguments.done, user['user'], user['token'])
  elif arguments.undone:
    undone(arguments.undone, user['user'], user['token'])
  elif arguments.ls:
    out = ls(user['user'], user['token'])
    display(out)
  elif arguments.remove:
    remove(arguments.remove, user['user'], user['token'])
  #except Exception as e:
  #  print e
  #  print 'Server is closed, please run it'
  #  exit(0)
  #print user


