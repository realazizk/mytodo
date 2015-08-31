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

import argparse
from sys import argv
from tools import *

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


