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
import thread
import random
import string
import sqlite3
import base64
import time
from tools import currdir
import sys

reload(sys)
sys.setdefaultencoding('utf8')

auth_user = {
  'user' : '',
  'token': ''
}

auth_users = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 7060))
sock.listen(10)
dbcon = sqlite3.connect(currdir('todo.db'), check_same_thread=False)
dbcon.text_factory = str

class database(object):

  def __init__(self, user, token):
    self.user=user
    self.token = token

  def ls(self):
    with dbcon:
      user=self._get_username(self.token)
      user_id=self._get_id_by_username(self.user)
      cur=dbcon.cursor()
      cur.execute('SELECT * FROM Todo WHERE owner=(?) AND done=0', (user_id,))
      return cur.fetchall()

  def listall(self):
    with dbcon:
      user = self._get_username(self.token)
      # get owner id
      user_id = self._get_id_by_username(self.user)
      cur = dbcon.cursor()
      cur.execute('SELECT * FROM Todo WHERE owner=(?)', (user_id,))
      return cur.fetchall()

  def add(self, todo):
    """
    todo method will add a new entry to the database
    todo object can be passed as a tuple or a list
    """
    with dbcon:
      cur = dbcon.cursor()
      cur.execute('INSERT INTO Todo VALUES(?, ?, ?, ?, ?)', todo)
      dbcon.commit()

  def check_token(self, token):
    return self.token == token

  def _get_username(self, token):
    """this will return the index in the list of the dict we are looking for"""
    #lst = next(index for (index, d) in enumerate(auth_users) if d['token']==token)
    for i, dic in enumerate(auth_users):
      if dic['token']==token:
        return auth_users[i]['user']
        break
      return False

  def done_undone(self, num, da=1):
    """
    this will mark todo as done ,
    using the number displayed to the user not the id
    """
    # this will get the id of the post

    hm = self.listall()
    iden = hm[int(num)][0]
    with dbcon:
      cur = dbcon.cursor()
      cur.execute('UPDATE Todo SET done=(?) WHERE id=(?)', (da,iden))
      dbcon.commit()

  def get_tag(self, tag):

    user_id=self._get_id_by_username(self.user)
    with dbcon:
      cur = dbcon.cursor()
      cur.execute('SELECT * FROM Todo WHERE owner=(?) AND todotext LIKE ?', ( user_id, '%'+tag+'%'))
      return cur.fetchall()

  def _get_id_by_username(self, user):
    with dbcon:
      cur = dbcon.cursor()
      cur.execute('SELECT id FROM Users WHERE username=(?)', (user,))
      return cur.fetchone()[0]

  def remove(self, num):
    hm = self.listall()
    iden = hm[int(num)][0]
    user_id=self._get_id_by_username(self.user)
    with dbcon:
      cur= dbcon.cursor()
      cur.execute('DELETE FROM Todo WHERE id=(?) AND owner=(?)', (iden,user_id))
      dbcon.commit()

def generate_token(length):
  pool = string.letters + string.digits
  return ''.join(random.choice(pool) for i in xrange(length))

def check_duplicated_users(user, auth_users):
  # ugly and non performant code
  found = False
  for elem in auth_users:
    if elem['user'] == user['user']:
      found = True
      break
  return found


def remove_quotes(st):
  # this will remove quotes or double quotes from a given string
  if st[0] in ['\'', '"'] and st[-1] in ['\'', '"']:
    return st[1:-1]
  else:
    return st

def workerthread(conn):
  while True:
    data= conn.recv(4096)
    if not data:
      break
    dat = data.split(' ', 3)
    if dat :
      if len(dat)>2 and check_duplicated_users({'user' : dat[1]}, auth_users):
        print time.strftime("Request Sent from "+dat[1] +" %Y-%m-%d %H:%M")
      if dat[0] == 'auth' :
        with dbcon:
          # Just logging in
          cur = dbcon.cursor()
          cur.execute('SELECT username,password FROM Users WHERE username=(?)', (dat[1],))
          data = cur.fetchone()
        if dat[1] == data[0] and dat[2] == data[1]:
          token = generate_token(64)
          if not token :
            conn.send('FAI')
            break
          conn.send('SUC')
          auth = auth_user
          auth['user'] = dat[1]
          auth['token'] = token
          del dat[:]

          # Don't reauthentificate users
          if not check_duplicated_users(auth, auth_users):
            auth_users.append(auth)
          # send back to the client the key
          conn.send(token)
        else :
          conn.send('FAI')
      elif dat[0] == 'lsall' and len(dat)==3:
        usr = database(dat[1], dat[2])
        a=usr.listall()
        conn.send(base64.b64encode(str(a)))
      elif dat[0] == 'add':
        # make the todo tuple
        usr = database(dat[1], dat[2])
        todotuple = (None, usr._get_id_by_username(dat[1]), dat[3], 0,
                     time.strftime('%Y/%m/%d %H:%M:%S'))
        usr.add(todotuple)
      elif dat[0] == 'done':
        usr=database(dat[1], dat[2])
        dat[3] = dat[3].split('\n')[0]
        usr.done_undone(dat[3])

      elif dat[0] == 'undone':
        usr=database(dat[1], dat[2])
        dat[3] = dat[3].split('\n')[0]
        usr.done_undone(dat[3], 0)
      elif dat[0] == 'ls':
        usr=database(dat[1], dat[2])
        a=usr.ls()
        conn.send(base64.b64encode(str(a)))
      elif dat[0] == 'remove':
        usr=database(dat[1], dat[2])
        dat[3] = dat[3].split('\n')[0]
        usr.remove(dat[3])
      elif dat[0] ==  'get_tag':
        usr = database(dat[1], dat[2])
        conn.send(base64.b64encode(str(usr.get_tag(dat[3]))))
  conn.close()

while True:
  try :
    conn, adr  = sock.accept()
    thread.start_new_thread(workerthread, (conn,))
  except KeyboardInterrupt :
    print 'Bye!'
    break
sock.close()

